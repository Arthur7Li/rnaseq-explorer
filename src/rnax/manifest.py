import hashlib
import platform
import subprocess
import sys
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from pydantic import BaseModel

from rnax.config import AnalysisConfig


class ReproducibilityManifest(BaseModel):
    rnax_version: str
    python_version: str
    platform: str
    packages: dict[str, str]
    git_commit: str | None
    config_sha256: str
    counts_sha256: str
    metadata_sha256: str
    timestamp: str
    random_seed: int
    command: str


def _sha256(path: Path) -> str:
    """Calculate the SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        # Read in chunks to handle large files
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _get_git_commit() -> str | None:
    """Attempt to retrieve the current git commit hash."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def build_manifest(config: AnalysisConfig, config_path: Path) -> ReproducibilityManifest:
    """Build a reproducibility manifest for the current execution."""
    packages_to_track = [
        "pydeseq2",
        "pandas",
        "pandera",
        "scikit-learn",
        "matplotlib",
        "seaborn",
        "jinja2",
    ]
    
    packages_versions = {}
    for pkg in packages_to_track:
        try:
            packages_versions[pkg] = version(pkg)
        except PackageNotFoundError:
            packages_versions[pkg] = "unknown"
            
    try:
        rnax_ver = version("rnax")
    except PackageNotFoundError:
        rnax_ver = "unknown"

    return ReproducibilityManifest(
        rnax_version=rnax_ver,
        python_version=sys.version.split(" ")[0],
        platform=platform.platform(),
        packages=packages_versions,
        git_commit=_get_git_commit(),
        config_sha256=_sha256(config_path),
        counts_sha256=_sha256(Path(config.input.counts)),
        metadata_sha256=_sha256(Path(config.input.metadata)),
        timestamp=datetime.now(timezone.utc).isoformat(),
        random_seed=config.output.random_seed,
        command=" ".join(sys.argv)
    )
