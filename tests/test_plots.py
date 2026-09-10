import pandas as pd
import pytest

from rnax.pipeline.plots import plot_library_sizes, plot_pca, plot_volcano


@pytest.fixture
def sample_counts():
    return pd.DataFrame({
        "sample1": [10, 20, 30],
        "sample2": [15, 25, 35],
    }, index=["gene1", "gene2", "gene3"])


@pytest.fixture
def sample_metadata():
    return pd.DataFrame({
        "sample_id": ["sample1", "sample2"],
        "condition": ["A", "B"],
    }).set_index("sample_id")


@pytest.fixture
def sample_results():
    return pd.DataFrame({
        "log2FoldChange": [1.5, -0.5, -2.0],
        "padj": [0.01, 0.5, 0.0001],
    }, index=["gene1", "gene2", "gene3"])


def test_plot_library_sizes(mocker, sample_counts, sample_metadata):
    mock_savefig = mocker.patch("rnax.pipeline.plots.plt.savefig")
    plot_library_sizes(sample_counts, sample_metadata, "condition", "test_lib.png")
    mock_savefig.assert_called_once_with("test_lib.png", dpi=300)


def test_plot_pca(mocker, sample_counts, sample_metadata):
    mock_savefig = mocker.patch("rnax.pipeline.plots.plt.savefig")
    plot_pca(sample_counts, sample_metadata, "condition", "test_pca.png")
    mock_savefig.assert_called_once_with("test_pca.png", dpi=300)


def test_plot_volcano(mocker, sample_results):
    mock_savefig = mocker.patch("rnax.pipeline.plots.plt.savefig")
    plot_volcano(sample_results, 0.05, 1.0, "test_volcano.png")
    mock_savefig.assert_called_once_with("test_volcano.png", dpi=300)

def test_plot_sample_distances(mocker, sample_counts, sample_metadata):
    mock_savefig = mocker.patch("rnax.pipeline.plots.plt.savefig")
    from rnax.pipeline.plots import plot_sample_distances
    plot_sample_distances(sample_counts, sample_metadata, "condition", None, "test_dist.png")
    mock_savefig.assert_called_once_with("test_dist.png", dpi=300, bbox_inches="tight")


def test_plot_sample_distances_with_block(mocker, sample_counts, sample_metadata):
    sample_metadata["block"] = ["b1", "b2"]
    mock_savefig = mocker.patch("rnax.pipeline.plots.plt.savefig")
    from rnax.pipeline.plots import plot_sample_distances
    plot_sample_distances(sample_counts, sample_metadata, "condition", "block", "test_dist.png")
    mock_savefig.assert_called_once_with("test_dist.png", dpi=300, bbox_inches="tight")


def test_plot_ma(mocker, sample_results):
    # Add baseMean to sample_results for MA plot
    sample_results["baseMean"] = [100, 10, 500]
    mock_savefig = mocker.patch("rnax.pipeline.plots.plt.savefig")
    from rnax.pipeline.plots import plot_ma
    plot_ma(sample_results, 0.05, 1.0, "test_ma.png")
    mock_savefig.assert_called_once_with("test_ma.png", dpi=300)


def test_plot_top_genes_heatmap(mocker, sample_counts, sample_results, sample_metadata):
    mock_savefig = mocker.patch("rnax.pipeline.plots.plt.savefig")
    from rnax.pipeline.plots import plot_top_genes_heatmap
    plot_top_genes_heatmap(sample_counts, sample_results, sample_metadata, "condition", None, 30, "test_heat.png")
    mock_savefig.assert_called_once_with("test_heat.png", dpi=300, bbox_inches="tight")


def test_plot_top_genes_heatmap_few_genes(mocker, sample_counts, sample_results, sample_metadata):
    # Test with fewer genes than n_top
    mock_savefig = mocker.patch("rnax.pipeline.plots.plt.savefig")
    from rnax.pipeline.plots import plot_top_genes_heatmap
    plot_top_genes_heatmap(sample_counts, sample_results, sample_metadata, "condition", None, 2, "test_heat_few.png")
    mock_savefig.assert_called_once_with("test_heat_few.png", dpi=300, bbox_inches="tight")

