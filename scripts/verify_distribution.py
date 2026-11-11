"""Validate built wheel/sdist scope; refuse missing or unexpected release payloads."""
from __future__ import annotations

import argparse
import email
import tarfile
import tomllib
import zipfile
from pathlib import Path, PurePosixPath

PACKAGE = "ai_security_labs"
def project_version() -> str:
    """Get the release identity from the single source of truth, pyproject.toml."""
    project_file = Path(__file__).resolve().parents[1] / "pyproject.toml"
    with project_file.open("rb") as handle:
        metadata = tomllib.load(handle).get("project", {})
    version = metadata.get("version")
    if not isinstance(version, str) or not version:
        raise ValueError("Project version unavailable")
    return version


VERSION = project_version()
REQUIRED_CODE = ("security_lab/agent_eval.py", "security_lab/agent_targets.py",
                 "security_lab/oracle.py", "scripts/verify_repro_bundle.py")


class DistributionError(ValueError):
    """Release archive is incomplete or contains forbidden content."""


def _safe(names: list[str]) -> None:
    if len(names) != len(set(names)):
        raise DistributionError("Duplicate archive entries")
    for name in names:
        parts = PurePosixPath(name).parts
        if not parts or name.startswith("/") or ".." in parts or "\\" in name:
            raise DistributionError("Unsafe archive path")
        if any(part in {"artifacts", ".git", "__pycache__", ".venv"} for part in parts):
            raise DistributionError("Forbidden generated/private release content")


def verify_distribution(directory: Path) -> dict[str, str]:
    wheels = sorted(directory.glob("*.whl"))
    sdists = sorted(directory.glob("*.tar.gz"))
    if len(wheels) != 1 or len(sdists) != 1:
        raise DistributionError("Expected exactly one wheel and one sdist")
    wheel, sdist = wheels[0], sdists[0]
    if not wheel.name.startswith(f"{PACKAGE}-{VERSION}-") or not sdist.name == f"ai_security_labs-{VERSION}.tar.gz":
        raise DistributionError("Unexpected distribution name/version")
    try:
        with zipfile.ZipFile(wheel) as archive:
            names = archive.namelist()
            _safe(names)
            if not all(name in names for name in REQUIRED_CODE):
                raise DistributionError("Wheel lacks required runnable modules")
            if any(name.startswith("tests/") for name in names):
                raise DistributionError("Wheel contains test package")
            metadata_path = f"{PACKAGE}-{VERSION}.dist-info/METADATA"
            if metadata_path not in names:
                raise DistributionError("Wheel lacks metadata")
            metadata = email.message_from_bytes(archive.read(metadata_path))
            if metadata.get("Name") != "ai-security-labs" or metadata.get("Version") != VERSION:
                raise DistributionError("Wheel metadata mismatch")
            if archive.testzip() is not None:
                raise DistributionError("Corrupt wheel member")
        with tarfile.open(sdist, "r:gz") as archive:
            members = archive.getmembers()
            _safe([member.name for member in members])
            prefix = f"ai_security_labs-{VERSION}/"
            names = {member.name for member in members if member.isfile()}
            required = {prefix + item for item in REQUIRED_CODE}
            required |= {prefix + item for item in ("README.md", "LICENSE", "pyproject.toml")}
            if not required.issubset(names):
                raise DistributionError("Sdist lacks code, license, or build metadata")
            if any(member.issym() or member.islnk() for member in members):
                raise DistributionError("Sdist contains links")
    except (zipfile.BadZipFile, tarfile.TarError, OSError, KeyError) as exc:
        raise DistributionError("Unreadable distribution archive") from exc
    return {"wheel": wheel.name, "sdist": sdist.name}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args(argv)
    try:
        result = verify_distribution(args.directory)
    except DistributionError as exc:
        parser.exit(1, f"DISTRIBUTION FAILED: {exc}\n")
    print("DISTRIBUTION PASS:", result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
