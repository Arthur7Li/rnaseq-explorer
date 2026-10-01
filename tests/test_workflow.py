import subprocess

import pytest

snakemake = pytest.importorskip("snakemake")

def test_snakemake_dryrun_pasilla() -> None:
    """Test that the Snakemake DAG builds correctly for Pasilla."""
    result = subprocess.run(
        ["uv", "run", "snakemake", "-n", "-F", "-s", "workflow/Snakefile", "--config", "rnax_config=config/pasilla.yaml"],
        capture_output=True,
        text=True, check=False
    )
    assert result.returncode == 0
    assert "Job stats:" in result.stdout

def test_snakemake_missing_config() -> None:
    """Test that a missing config fails gracefully."""
    result = subprocess.run(
        ["uv", "run", "snakemake", "-n", "-s", "workflow/Snakefile", "--config", "rnax_config=config/missing.yaml"],
        capture_output=True,
        text=True, check=False
    )
    assert result.returncode != 0

