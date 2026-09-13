from pathlib import Path

import pandas as pd
import pytest

from rnax.config import AnalysisConfig
from rnax.pipeline.report import generate_report


@pytest.fixture
def mock_config(tmp_path):
    config = AnalysisConfig.model_construct()
    config.output = type("obj", (object,), {"directory": str(tmp_path), "report_title": "Test Title"})()
    config.design = type("obj", (object,), {
        "condition_column": "condition",
        "paired_or_block_column": "batch",
        "reference_level": "A",
        "comparison_level": "B"
    })()
    config.thresholds = type("obj", (object,), {
        "fdr": 0.05,
        "absolute_log2_fold_change": 1.0,
        "top_n_genes": 30
    })()
    config.input = type("obj", (object,), {
        "counts": "mock_counts.csv",
        "metadata": "mock_metadata.csv"
    })()
    config.dataset_limitations = ["Test limitation 1", "Test limitation 2"]
    return config


@pytest.fixture
def dummy_dfs():
    counts = pd.DataFrame({"sample1": [10], "sample2": [20]}, index=["gene1"])
    metadata = pd.DataFrame({"condition": ["A", "B"]}, index=["sample1", "sample2"])
    results = pd.DataFrame({"log2FoldChange": [1.5], "padj": [0.01]}, index=["gene1"])
    return counts, metadata, counts, results


def test_generate_report(mocker, mock_config, dummy_dfs):
    raw_counts, metadata, norm_counts, results = dummy_dfs
    
    # Mock plotting functions so we don't actually draw plots during tests
    mocker.patch("rnax.pipeline.report.plot_library_sizes")
    mocker.patch("rnax.pipeline.report.plot_pca")
    mocker.patch("rnax.pipeline.report.plot_volcano")
    mocker.patch("rnax.pipeline.report.plot_sample_distances")
    mocker.patch("rnax.pipeline.report.plot_ma")
    mocker.patch("rnax.pipeline.report.plot_top_genes_heatmap")
    
    from rnax.manifest import ReproducibilityManifest
    mock_manifest = ReproducibilityManifest(
        rnax_version="0.1.0",
        python_version="3.13",
        platform="Darwin",
        packages={"pandas": "1.0"},
        git_commit="abc",
        config_sha256="config_hash",
        counts_sha256="counts_hash",
        metadata_sha256="meta_hash",
        timestamp="2026-09-02T00:00:00Z",
        random_seed=42,
        command="rnax analyze my_config.yaml"
    )
    
    from rnax.pipeline.deseq import FilteringResult
    mock_filtering = FilteringResult(
        filtered_counts=raw_counts,
        genes_before=100,
        genes_after=80,
        min_count=10,
        min_samples=2,
    )
    
    generate_report(mock_config, raw_counts, metadata, norm_counts, results, mock_manifest, mock_filtering)
    
    out_dir = Path(mock_config.output.directory)
    
    assert (out_dir / "results.csv").exists()
    assert (out_dir / "normalized_counts.csv").exists()
    
    report_path = out_dir / "report.html"
    assert report_path.exists()
    
    html = report_path.read_text()
    
    # Verify contents
    assert "Test Title" in html
    assert "exploratory, non-clinical" in html
    assert "condition" in html
    assert "batch" in html
    assert "Pre-filtering Summary" in html
    assert "Genes before filtering:</strong> 100" in html
    assert "Genes after filtering:</strong> 80" in html
    assert "Genes removed:</strong> 20" in html
    assert "Threshold Interpretation" in html
    
    # Verify Phase 8 additions
    assert "Data Provenance" in html
    assert "config_hash" in html
    assert "mock_counts.csv" in html
    
    assert "QC Observations" in html
    assert "This is an observational assessment of data structure, not a causal conclusion" in html
    
    assert "Methodology" in html
    assert "Negative binomial GLM" in html or "negative binomial distribution" in html
    assert "Median-of-ratios" in html
    
    assert "Dataset-Specific Limitations" in html
    assert "Test limitation 1" in html
    
    assert "General Limitations" in html
    assert "No Causal Claims" in html
    
    assert "How to Reproduce" in html
    assert "rnax analyze my_config.yaml" in html


def test_report_no_dataset_limitations(mocker, mock_config, dummy_dfs):
    # Test that the dataset limitations section is omitted if empty
    mock_config.dataset_limitations = []
    raw_counts, metadata, norm_counts, results = dummy_dfs
    
    for plot_fn in ["plot_library_sizes", "plot_pca", "plot_volcano", "plot_sample_distances", "plot_ma", "plot_top_genes_heatmap"]:
        mocker.patch(f"rnax.pipeline.report.{plot_fn}")
        
    from rnax.manifest import ReproducibilityManifest
    mock_manifest = ReproducibilityManifest(
        rnax_version="0.1.0", python_version="3.13", platform="Darwin", packages={},
        git_commit=None, config_sha256="", counts_sha256="", metadata_sha256="",
        timestamp="", random_seed=42, command=""
    )
    
    from rnax.pipeline.deseq import FilteringResult
    mock_filtering = FilteringResult(filtered_counts=raw_counts, genes_before=0, genes_after=0, min_count=0, min_samples=0)
    
    generate_report(mock_config, raw_counts, metadata, norm_counts, results, mock_manifest, mock_filtering)
    
    out_dir = Path(mock_config.output.directory)
    html = (out_dir / "report.html").read_text()
    
    assert "Dataset-Specific Limitations" not in html
    assert "Test limitation 1" not in html
