"""Offline regression tests for deterministic source release integrity."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.release_bundle import ReleaseError, create, verify


class ReleaseBundleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        for args in (("init", "-q"), ("config", "user.email", "test@example.invalid"),
                     ("config", "user.name", "Release Test")):
            subprocess.run(["git", "-C", str(self.repo), *args], check=True, capture_output=True)
        (self.repo / "pyproject.toml").write_text("[project]\nname = 'test'\n", encoding="utf-8")
        (self.repo / "module.py").write_text("x = 1\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.repo), "add", "."], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(self.repo), "commit", "-qm", "initial"],
                       check=True, capture_output=True)
        self.archive = self.root / "source.zip"
        self.manifest = self.root / "manifest.json"

    def test_create_verify_and_deterministic_bytes(self):
        first = create(self.repo, self.archive, self.manifest)
        original = self.archive.read_bytes()
        self.assertEqual(first["commit"], verify(self.archive, self.manifest)["commit"])
        create(self.repo, self.archive, self.manifest)
        self.assertEqual(original, self.archive.read_bytes())

    def test_modified_tracked_source_rejected(self):
        (self.repo / "module.py").write_text("x = 2\n", encoding="utf-8")
        with self.assertRaises(ReleaseError):
            create(self.repo, self.archive, self.manifest)

    def test_untracked_file_rejected(self):
        (self.repo / "secret.txt").write_text("not for release", encoding="utf-8")
        with self.assertRaises(ReleaseError):
            create(self.repo, self.archive, self.manifest)

    def test_tamper_archive_rejected(self):
        create(self.repo, self.archive, self.manifest)
        self.archive.write_bytes(self.archive.read_bytes() + b"extra")
        with self.assertRaises(ReleaseError):
            verify(self.archive, self.manifest)

    def test_modified_manifest_rejected(self):
        create(self.repo, self.archive, self.manifest)
        data = json.loads(self.manifest.read_text(encoding="utf-8"))
        data["files"]["module.py"] = "0" * 64
        self.manifest.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaises(ReleaseError):
            verify(self.archive, self.manifest)

    def test_symlink_rejected(self):
        (self.repo / "link").symlink_to("module.py")
        subprocess.run(["git", "-C", str(self.repo), "add", "link"],
                       check=True, capture_output=True)
        subprocess.run(["git", "-C", str(self.repo), "commit", "-qm", "link"],
                       check=True, capture_output=True)
        with self.assertRaises(ReleaseError):
            create(self.repo, self.archive, self.manifest)


if __name__ == "__main__":
    unittest.main()
