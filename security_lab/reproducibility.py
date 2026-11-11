"""Fail-closed, privacy-limited provenance and artifact integrity evidence.

The runner deliberately stores no prompts, model outputs, canary values, or
environment variables. Host metadata is intentionally coarse, not a full
hardware fingerprint. This is experiment traceability, not bitwise replay.
"""

from __future__ import annotations

import hashlib
import json
import platform
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


class ProvenanceError(ValueError):
    """Required reproducibility evidence is missing or ambiguous."""


def _git(repo: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ['git', '-C', str(repo), *args], capture_output=True, text=True,
            timeout=10, check=True,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise ProvenanceError('Cannot verify local Git state') from exc
    return result.stdout.strip()


def git_provenance(repo: Path) -> dict[str, Any]:
    """Require a real repository root, HEAD and clean tracked source files."""
    root = Path(_git(repo, 'rev-parse', '--show-toplevel')).resolve()
    if root != repo.resolve():
        raise ProvenanceError('Run from the root of the Git repository')
    commit = _git(repo, 'rev-parse', '--verify', 'HEAD')
    if not re.fullmatch(r'[0-9a-f]{40,64}', commit):
        raise ProvenanceError('Invalid source commit')
    tracked_changes = _git(repo, 'status', '--porcelain', '--untracked-files=no')
    if tracked_changes:
        raise ProvenanceError('Tracked source changes must be committed before live evaluation')
    return {'commit': commit, 'tracked_tree_clean': True}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def collect_metadata(model: Any, repo: Path, *, repeats: int) -> dict[str, Any]:
    """Obtain authoritative local Ollama tag digest and server version.

    Requires a client implementing ``identity``. Never fall back to model
    name as a digest. The endpoint's path is omitted from persisted evidence.
    """
    identity = model.identity()
    if not isinstance(identity, dict):
        raise ProvenanceError('Invalid model identity')
    digest = identity.get('model_digest')
    version = identity.get('ollama_version')
    if not isinstance(digest, str) or not re.fullmatch(r'(?:sha256:)?[0-9a-f]{64}', digest):
        raise ProvenanceError('Immutable model digest unavailable')
    if not isinstance(version, str) or not version.strip() or len(version) > 128:
        raise ProvenanceError('Ollama version unavailable')
    git = git_provenance(repo)
    endpoint = urlsplit(model.endpoint)
    return {
        'schema_version': 1,
        'collected_at_utc': datetime.now(timezone.utc).isoformat(),
        'git': git,
        'model': {'name': model.model, 'digest_sha256': digest.removeprefix('sha256:'), 'ollama_version': version},
        'runtime': {
            'python_version': platform.python_version(),
            'python_implementation': platform.python_implementation(),
            'os': platform.system(), 'os_release': platform.release(),
            'architecture': platform.machine(),
            'ollama_transport': 'http_loopback',
            'ollama_port': endpoint.port or 80,
        },
        'experiment': {
            'repeats': repeats,
            'temperature': 0,
            'num_predict': 256,
            'marker_random_bits': 96,
            'target': 'same_model_response_before_after_output_filter',
            'single_turn_per_case': True,
        },
    }


def write_manifest(path: Path, json_report: Path, html_report: Path, metadata: dict, result: dict) -> None:
    """Write a detached manifest. No recursive self-hash or absolute paths."""
    if len({p.resolve() for p in (path, json_report, html_report)}) != 3:
        raise ProvenanceError('Manifest and report paths must be distinct')
    for report in (json_report, html_report):
        if not report.is_file():
            raise ProvenanceError('Report missing')
    content = {
        'schema_version': 1,
        'metadata': metadata,
        'result': {'run_id': result['run_id'], 'gate': result['gate'], 'requests': result['metrics']['requests']},
        'artifacts': {
            'json': {'filename': json_report.name, 'sha256': sha256_file(json_report)},
            'html': {'filename': html_report.name, 'sha256': sha256_file(html_report)},
        },
        'integrity_note': 'Hashes cover exact report bytes; this unsigned manifest is not an authenticity attestation.',
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(content, indent=2, sort_keys=True) + '\n', encoding='utf-8')


def verify_manifest(path: Path, json_report: Path, html_report: Path) -> None:
    """Reject missing artifacts, malformed provenance and changed report bytes."""
    try:
        content = json.loads(path.read_text(encoding='utf-8'))
        if content['schema_version'] != 1:
            raise ProvenanceError('Unknown manifest schema')
        data = json.loads(json_report.read_text(encoding='utf-8'))
        if content['result']['run_id'] != data['run_id'] or content['result']['gate'] != data['gate']:
            raise ProvenanceError('Report identity does not match manifest')
        git = content['metadata']['git']
        model = content['metadata']['model']
        if not git['tracked_tree_clean'] or not re.fullmatch(r'[0-9a-f]{40,64}', git['commit']):
            raise ProvenanceError('Invalid Git provenance')
        if not re.fullmatch(r'[0-9a-f]{64}', model['digest_sha256']) or not model['ollama_version']:
            raise ProvenanceError('Invalid model provenance')
        for label, report in [('json', json_report), ('html', html_report)]:
            entry = content['artifacts'][label]
            if entry['filename'] != report.name or entry['sha256'] != sha256_file(report):
                raise ProvenanceError(f'{label.upper()} report digest mismatch')
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        raise ProvenanceError('Invalid reproducibility bundle') from exc
