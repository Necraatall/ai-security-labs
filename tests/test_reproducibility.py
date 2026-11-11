"""Offline tests of provenance, model metadata and fail-closed evidence integrity."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from security_lab.ollama import OllamaClient
from security_lab.reproducibility import (
    ProvenanceError, collect_metadata, git_provenance, verify_manifest,
    write_manifest,
)


DIGEST = 'a' * 64
COMMIT = 'b' * 40


class FakeClient:
    model = 'example:latest'
    endpoint = 'http://127.0.0.1:11434'

    def identity(self):
        return {'model_digest': DIGEST, 'ollama_version': '0.12.0'}


class TestModelIdentity(unittest.TestCase):
    def test_identity(self):
        client = OllamaClient('example:latest')
        def source(route):
            if route == '/api/version':
                return {'version': '0.12.0'}
            return {'models': [{'name': 'other:latest', 'digest': 'c' * 64},
                               {'name': 'example:latest', 'digest': DIGEST}]}
        with patch.object(client.__class__, '_get_json', side_effect=source):
            self.assertEqual(client.identity()['model_digest'], DIGEST)

    def test_missing_exact_tag_fails(self):
        client = OllamaClient('example:latest')
        with patch.object(client.__class__, '_get_json', side_effect=lambda route: (
            {'version': '0.12.0'} if route == '/api/version' else {'models': []}
        )):
            with self.assertRaises(ProvenanceError):
                client.identity()


class TestReproducibility(unittest.TestCase):
    def metadata(self):
        with patch('security_lab.reproducibility.git_provenance', return_value={
            'commit': COMMIT, 'tracked_tree_clean': True
        }):
            return collect_metadata(FakeClient(), Path('.'), repeats=3)

    def test_metadata(self):
        metadata = self.metadata()
        self.assertEqual(metadata['model']['digest_sha256'], DIGEST)
        self.assertEqual(metadata['experiment']['repeats'], 3)
        self.assertNotIn('LABCANARY-', repr(metadata))

    def test_invalid_model_digest_rejected(self):
        class Invalid(FakeClient):
            def identity(self):
                return {'model_digest': 'unknown', 'ollama_version': '0.12.0'}
        with self.assertRaises(ProvenanceError):
            collect_metadata(Invalid(), Path('.'), repeats=1)

    def test_manifest_and_tamper(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            json_path, html_path, manifest = root/'result.json', root/'result.html', root/'manifest.json'
            result = {'run_id': 'abc', 'gate': 'BLOCK', 'metrics': {'requests': 4}}
            json_path.write_text(json.dumps(result))
            html_path.write_text('<html></html>')
            write_manifest(manifest, json_path, html_path, self.metadata(), result)
            verify_manifest(manifest, json_path, html_path)
            html_path.write_text('<html>tampered</html>')
            with self.assertRaises(ProvenanceError):
                verify_manifest(manifest, json_path, html_path)

    def test_identical_paths_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(ProvenanceError):
                write_manifest(root/'a', root/'a', root/'b', self.metadata(), {})

    def test_git_no_git_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ProvenanceError):
                git_provenance(Path(tmp))


if __name__ == '__main__':
    unittest.main()
