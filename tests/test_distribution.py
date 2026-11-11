"""Fail-closed checks for release-archive validation."""
from __future__ import annotations

import io
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.verify_distribution import DistributionError, verify_distribution


class DistributionTests(unittest.TestCase):
    def make_archive(self, destination: Path, *, missing: bool = False,
                     forbidden: bool = False) -> None:
        package = "ai_security_labs"
        version = "0.10.0"
        code = ("security_lab/agent_eval.py", "security_lab/agent_targets.py",
                "security_lab/oracle.py", "scripts/verify_repro_bundle.py")
        with zipfile.ZipFile(destination / f"{package}-{version}-py3-none-any.whl", "w") as wheel:
            for name in code[:3] if missing else code:
                wheel.writestr(name, "# test\n")
            wheel.writestr(f"{package}-{version}.dist-info/METADATA",
                           f"Name: ai-security-labs\nVersion: {version}\n")
            if forbidden:
                wheel.writestr("artifacts/private.json", "{}")
        with tarfile.open(destination / f"{package}-{version}.tar.gz", "w:gz") as sdist:
            for name in (*code, "README.md", "LICENSE", "pyproject.toml"):
                raw = b"test\n"
                member = tarfile.TarInfo(f"{package}-{version}/{name}")
                member.size = len(raw)
                sdist.addfile(member, io.BytesIO(raw))

    def test_valid_archive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            self.make_archive(path)
            self.assertEqual(len(verify_distribution(path)), 2)

    def test_missing_wheel_module_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            self.make_archive(path, missing=True)
            with self.assertRaises(DistributionError):
                verify_distribution(path)

    def test_forbidden_artifact_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            self.make_archive(path, forbidden=True)
            with self.assertRaises(DistributionError):
                verify_distribution(path)

    def test_missing_archive_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(DistributionError):
                verify_distribution(Path(directory))


if __name__ == "__main__":
    unittest.main()
