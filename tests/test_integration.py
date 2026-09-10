from pathlib import Path

import pytest
from typer.testing import CliRunner

from rnax.cli import app


@pytest.fixture(scope="module")
def setup_pasilla_test_data(tmp_path_factory):
    """
    Sets up a temporary directory with the pasilla configuration
    so we don't overwrite user's actual results/pasilla dir during testing.
    """
    # Use a temporary output directory
    temp_dir = tmp_path_factory.mktemp("pasilla_integration")
    out_dir = temp_dir / "results"
    
    # We will invoke the CLI by overriding the output directory dynamically, 
    # but currently RNA-seq explorer CLI doesn't support overriding output dir 
    # via CLI flag. So we will create a temporary config file that points to temp_dir.
    
    config_path = temp_dir / "pasilla_test.yaml"
    import yaml
    
    config_content = {
        "input": {
            "counts": "data/pasilla/counts.csv",
            "metadata": "data/pasilla/metadata.csv",
            "gene_id_column": "gene_id"
        },
        "design": {
            "condition_column": "condition",
            "reference_level": "untreated",
            "comparison_level": "treated"
        },
        "filtering": {
            "minimum_count": 10,
            "minimum_samples": 2
        },
        "thresholds": {
            "fdr": 0.05,
            "absolute_log2_fold_change": 1.0,
            "top_n_genes": 30
        },
        "output": {
            "directory": str(out_dir),
            "report_title": "Integration Test Title"
        }
    }
    
    with open(config_path, "w") as f:
        yaml.dump(config_content, f)
        
    return config_path, out_dir


@pytest.mark.slow
def test_pasilla_integration(setup_pasilla_test_data):
    """
    End-to-end integration test using the Pasilla test dataset.
    This test runs the full PyDESeq2 pipeline and checks all outputs.
    """
    # Check if Pasilla dataset exists; if not, skip test to avoid CI hanging if data wasn't downloaded
    if not Path("data/pasilla/counts.csv").exists():
        pytest.skip("Pasilla test data not found. Run scripts/acquire_pasilla.py first.")
        
    config_path, out_dir = setup_pasilla_test_data
    
    runner = CliRunner()
    result = runner.invoke(app, ["analyze", "--config", str(config_path)])
    
    assert result.exit_code == 0
    assert "Successfully validated" in result.output
    assert "Differential expression complete" in result.output
    
    # Verify outputs exist
    assert (out_dir / "results.csv").exists()
    assert (out_dir / "normalized_counts.csv").exists()
    
    # Verify plots
    assert (out_dir / "library_sizes.png").exists()
    assert (out_dir / "pca.png").exists()
    assert (out_dir / "volcano.png").exists()
    assert (out_dir / "sample_distances.png").exists()
    assert (out_dir / "ma_plot.png").exists()
    assert (out_dir / "top_genes_heatmap.png").exists()
    
    # Verify report HTML
    report_path = out_dir / "report.html"
    assert report_path.exists()
    
    html = report_path.read_text()
    assert "Integration Test Title" in html
    assert "Pre-filtering Summary" in html
    assert "Threshold Interpretation" in html
