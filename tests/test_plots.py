from typing import Any

import pandas as pd
import pytest

from rnax.pipeline.plots import CB_PALETTE, WONG_PALETTE, plot_library_sizes, plot_pca, plot_volcano


@pytest.fixture
def sample_counts() -> Any:
    return pd.DataFrame({
        "sample1": [10, 20, 30],
        "sample2": [15, 25, 35],
    }, index=["gene1", "gene2", "gene3"])


@pytest.fixture
def sample_metadata() -> Any:
    return pd.DataFrame({
        "sample_id": ["sample1", "sample2"],
        "condition": ["A", "B"],
    }).set_index("sample_id")


@pytest.fixture
def sample_results() -> Any:
    return pd.DataFrame({
        "log2FoldChange": [1.5, -0.5, -2.0],
        "padj": [0.01, 0.5, 0.0001],
    }, index=["gene1", "gene2", "gene3"])


def test_cb_palette_wong() -> None:
    assert CB_PALETTE["Up"] == "#D55E00"
    assert CB_PALETTE["Down"] == "#0072B2"
    assert CB_PALETTE["Not Significant"] == "#999999"
    assert len(WONG_PALETTE) >= 7


def test_plot_library_sizes(mocker: Any, sample_counts: Any, sample_metadata: Any) -> None:
    mock_savefig = mocker.patch("rnax.pipeline.plots.plt.savefig")
    alt = plot_library_sizes(sample_counts, sample_metadata, "condition", "test_lib.png")
    mock_savefig.assert_called_once_with("test_lib.png", dpi=300)
    assert isinstance(alt, str)
    assert "library sizes" in alt.lower()


def test_plot_pca(mocker: Any, sample_counts: Any, sample_metadata: Any) -> None:
    mock_savefig = mocker.patch("rnax.pipeline.plots.plt.savefig")
    alt = plot_pca(sample_counts, sample_metadata, "condition", "test_pca.png")
    mock_savefig.assert_called_once_with("test_pca.png", dpi=300)
    assert isinstance(alt, str)
    assert "pca" in alt.lower() or "principal component" in alt.lower()


def test_plot_volcano(mocker: Any, sample_results: Any) -> None:
    mock_savefig = mocker.patch("rnax.pipeline.plots.plt.savefig")
    alt = plot_volcano(sample_results, 0.05, 1.0, "test_volcano.png")
    mock_savefig.assert_called_once_with("test_volcano.png", dpi=300)
    assert isinstance(alt, str)
    assert "volcano" in alt.lower()
    assert "vermillion" in alt.lower()
    assert "blue" in alt.lower()


def test_plot_sample_distances(mocker: Any, sample_counts: Any, sample_metadata: Any) -> None:
    mock_savefig = mocker.patch("rnax.pipeline.plots.plt.savefig")
    from rnax.pipeline.plots import plot_sample_distances
    alt = plot_sample_distances(sample_counts, sample_metadata, "condition", None, "test_dist.png")
    mock_savefig.assert_called_once_with("test_dist.png", dpi=300, bbox_inches="tight")
    assert isinstance(alt, str)
    assert "distance" in alt.lower()


def test_plot_sample_distances_with_block(mocker: Any, sample_counts: Any, sample_metadata: Any) -> None:
    sample_metadata["block"] = ["b1", "b2"]
    mock_savefig = mocker.patch("rnax.pipeline.plots.plt.savefig")
    from rnax.pipeline.plots import plot_sample_distances
    alt = plot_sample_distances(sample_counts, sample_metadata, "condition", "block", "test_dist.png")
    mock_savefig.assert_called_once_with("test_dist.png", dpi=300, bbox_inches="tight")
    assert isinstance(alt, str)


def test_plot_ma(mocker: Any, sample_results: Any) -> None:
    # Add baseMean to sample_results for MA plot
    sample_results["baseMean"] = [100, 10, 500]
    mock_savefig = mocker.patch("rnax.pipeline.plots.plt.savefig")
    from rnax.pipeline.plots import plot_ma
    alt = plot_ma(sample_results, 0.05, 1.0, "test_ma.png")
    mock_savefig.assert_called_once_with("test_ma.png", dpi=300)
    assert isinstance(alt, str)
    assert "ma plot" in alt.lower()


def test_plot_top_genes_heatmap(mocker: Any, sample_counts: Any, sample_results: Any, sample_metadata: Any) -> None:
    mock_savefig = mocker.patch("rnax.pipeline.plots.plt.savefig")
    from rnax.pipeline.plots import plot_top_genes_heatmap
    alt = plot_top_genes_heatmap(sample_counts, sample_results, sample_metadata, "condition", None, 30, "test_heat.png")
    mock_savefig.assert_called_once_with("test_heat.png", dpi=300, bbox_inches="tight")
    assert isinstance(alt, str)
    assert "heatmap" in alt.lower()


def test_plot_top_genes_heatmap_few_genes(mocker: Any, sample_counts: Any, sample_results: Any, sample_metadata: Any) -> None:
    # Test with fewer genes than n_top
    mock_savefig = mocker.patch("rnax.pipeline.plots.plt.savefig")
    from rnax.pipeline.plots import plot_top_genes_heatmap
    alt = plot_top_genes_heatmap(sample_counts, sample_results, sample_metadata, "condition", None, 2, "test_heat_few.png")
    mock_savefig.assert_called_once_with("test_heat_few.png", dpi=300, bbox_inches="tight")
    assert isinstance(alt, str)

