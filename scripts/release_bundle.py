"""Create and verify a deterministic, unsigned source archive from a Git commit.

The archive is rebuilt from committed Git blobs, not from working-tree files.
No local experiments, ignored artifacts, credentials, or uncommitted edits are used.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path, PurePosixPath

MAX_FILE_BYTES = 8 * 1024 * 1024
MAX_ARCHIVE_BYTES = 32 * 1024 * 1024
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
COMMIT_RE = re.compile(r"[0-9a-f]{40,64}\Z")


class ReleaseError(ValueError):
    """A release artifact or its source state violates the release contract."""


def _git(repo: Path, *args: str) -> bytes:
    try:
        return subprocess.run(
            ["git", "-C", str(repo), *args], capture_output=True, check=True,
            timeout=30,
        ).stdout
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise ReleaseError("Git source verification failed") from exc


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _safe_path(value: str) -> bool:
    path = PurePosixPath(value)
    return (
        bool(value) and not value.startswith("/") and "\\" not in value
        and all(part not in {"", ".", ".."} for part in value.split("/"))
        and not path.is_absolute()
    )


def committed_files(repo: Path) -> tuple[str, dict[str, bytes]]:
    """Read a clean repository's exact HEAD snapshot with strict regular-file modes."""
    root = Path(_git(repo, "rev-parse", "--show-toplevel").decode().strip()).resolve()
    if root != repo.resolve():
        raise ReleaseError("Repository path must be the Git root")
    if _git(repo, "status", "--porcelain"):
        raise ReleaseError("Commit or remove all non-ignored working-tree changes first")
    commit = _git(repo, "rev-parse", "HEAD").decode().strip()
    if not COMMIT_RE.fullmatch(commit):
        raise ReleaseError("Invalid commit identifier")
    output = _git(repo, "ls-tree", "-rz", "--full-tree", "HEAD")
    files: dict[str, bytes] = {}
    total = 0
    for item in output.split(b"\0"):
        if not item:
            continue
        try:
            header, raw_path = item.split(b"\t", 1)
            mode, kind, blob = header.decode("ascii").split(" ")
            name = raw_path.decode("utf-8")
        except (UnicodeDecodeError, ValueError) as exc:
            raise ReleaseError("Invalid Git tree entry") from exc
        if kind != "blob" or mode not in {"100644", "100755"} or not _safe_path(name):
            raise ReleaseError("Unsupported file type or path in Git tree")
        if name in files:
            raise ReleaseError("Duplicate Git tree path")
        data = _git(repo, "cat-file", "blob", blob)
        if len(data) > MAX_FILE_BYTES:
            raise ReleaseError("Source file size limit exceeded")
        total += len(data)
        if total > MAX_ARCHIVE_BYTES:
            raise ReleaseError("Source archive size limit exceeded")
        files[name] = data
    if not files or "pyproject.toml" not in files:
        raise ReleaseError("No valid Python project source snapshot")
    return commit, files


def _zip_bytes(files: dict[str, bytes]) -> bytes:
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
        for name in sorted(files):
            if not _safe_path(name):
                raise ReleaseError("Unsafe archive path")
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, files[name])
    return output.getvalue()


def create(repo: Path, archive: Path, manifest: Path) -> dict:
    """Create a deterministic release ZIP and detached machine-verifiable manifest."""
    if archive.resolve() == manifest.resolve():
        raise ReleaseError("Archive and manifest must have distinct paths")
    commit, files = committed_files(repo)
    content = _zip_bytes(files)
    if len(content) > MAX_ARCHIVE_BYTES:
        raise ReleaseError("Archive size limit exceeded")
    result = {
        "schema_version": 1,
        "kind": "unsigned_committed_source_release",
        "commit": commit,
        "archive": {"filename": archive.name, "sha256": _digest(content)},
        "files": {name: _digest(data) for name, data in sorted(files.items())},
        "limitations": "Unsigned source integrity evidence; not a model-run attestation or binary-reproducible environment.",
    }
    archive.parent.mkdir(parents=True, exist_ok=True)
    manifest.parent.mkdir(parents=True, exist_ok=True)
    archive.write_bytes(content)
    manifest.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    verify(archive, manifest)
    return result


def verify(archive: Path, manifest: Path) -> dict:
    """Verify archive digest, all file digests, paths, membership and canonical bytes."""
    try:
        result = json.loads(manifest.read_text(encoding="utf-8"))
        content = archive.read_bytes()
        if len(content) > MAX_ARCHIVE_BYTES:
            raise ReleaseError("Archive size limit exceeded")
        if (not isinstance(result, dict) or result.get("schema_version") != 1
                or result.get("kind") != "unsigned_committed_source_release"
                or not isinstance(result.get("commit"), str)
                or not COMMIT_RE.fullmatch(result["commit"])):
            raise ReleaseError("Invalid release manifest identity")
        entry = result["archive"]
        if (not isinstance(entry, dict) or entry.get("filename") != archive.name
                or entry.get("sha256") != _digest(content)):
            raise ReleaseError("Release archive digest mismatch")
        hashes = result["files"]
        if (not isinstance(hashes, dict) or not hashes or "pyproject.toml" not in hashes
                or any(not isinstance(k, str) or not _safe_path(k)
                       or not isinstance(v, str) or not SHA256_RE.fullmatch(v)
                       for k, v in hashes.items())):
            raise ReleaseError("Invalid source file digest inventory")
        with zipfile.ZipFile(io.BytesIO(content)) as bundle:
            info = bundle.infolist()
            names = [item.filename for item in info]
            if (names != sorted(hashes) or len(names) != len(set(names))
                    or any(item.is_dir() or item.file_size > MAX_FILE_BYTES
                           or item.compress_type != zipfile.ZIP_STORED for item in info)):
                raise ReleaseError("Unexpected or unsafe source archive membership")
            extracted = {name: bundle.read(name) for name in names}
            if any(_digest(data) != hashes[name] for name, data in extracted.items()):
                raise ReleaseError("Source file hash mismatch")
            if _zip_bytes(extracted) != content:
                raise ReleaseError("Archive does not have canonical deterministic encoding")
    except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile,
            zipfile.LargeZipFile, UnicodeError) as exc:
        raise ReleaseError("Invalid release bundle") from exc
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("create", "verify"))
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        result = (create(args.repo, args.archive, args.manifest) if args.action == "create"
                  else verify(args.archive, args.manifest))
    except ReleaseError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"PASS: {result['kind']}; commit={result['commit']}; files={len(result['files'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
