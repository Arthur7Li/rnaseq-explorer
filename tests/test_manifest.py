import hashlib

from rnax.config import AnalysisConfig
from rnax.manifest import _get_git_commit, _sha256, build_manifest


def test_sha256(tmp_path):
    test_file = tmp_path / "test.txt"
    content = b"hello world"
    test_file.write_bytes(content)
    
    expected_hash = hashlib.sha256(content).hexdigest()
    assert _sha256(test_file) == expected_hash


def test_get_git_commit(mocker):
    # Test successful git execution
    mock_run = mocker.patch("rnax.manifest.subprocess.run")
    mock_run.return_value.stdout = "abcdef123456\n"
    assert _get_git_commit() == "abcdef123456"
    
    # Test git error
    import subprocess
    mock_run.side_effect = subprocess.CalledProcessError(1, ["git"])
    assert _get_git_commit() is None
    
    # Test file not found (git not installed)
    mock_run.side_effect = FileNotFoundError()
    assert _get_git_commit() is None


def test_build_manifest(tmp_path, mocker):
    # Create mock files
    config_file = tmp_path / "config.yaml"
    counts_file = tmp_path / "counts.csv"
    meta_file = tmp_path / "meta.csv"
    
    config_file.write_text("config")
    counts_file.write_text("counts")
    meta_file.write_text("meta")
    
    config = AnalysisConfig.model_construct()
    config.input = type("obj", (object,), {
        "counts": str(counts_file),
        "metadata": str(meta_file),
    })()
    config.output = type("obj", (object,), {
        "random_seed": 42
    })()
    
    manifest = build_manifest(config, config_file)
    
    assert manifest.config_sha256 == _sha256(config_file)
    assert manifest.counts_sha256 == _sha256(counts_file)
    assert manifest.metadata_sha256 == _sha256(meta_file)
    
    assert manifest.random_seed == 42
    assert "pydeseq2" in manifest.packages
    assert "pandas" in manifest.packages
    assert manifest.python_version
    assert manifest.platform
    assert manifest.timestamp
    assert manifest.command
