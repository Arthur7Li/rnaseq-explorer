import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA


def plot_library_sizes(counts_df: pd.DataFrame, metadata_df: pd.DataFrame, condition_col: str, output_path: str):
    """
    Plot library sizes (total reads per sample).
    """
    sizes = counts_df.sum(axis=0)
    plot_df = pd.DataFrame({
        "Sample": sizes.index,
        "Library Size": sizes.values,
        "Condition": metadata_df.loc[sizes.index, condition_col].values
    })
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=plot_df, x="Sample", y="Library Size", hue="Condition", dodge=False)
    plt.title("Library Sizes per Sample")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_pca(normalized_counts: pd.DataFrame, metadata_df: pd.DataFrame, condition_col: str, output_path: str):
    """
    Plot PCA of log1p transformed normalized counts.
    normalized_counts: genes x samples
    """
    # log1p transform to stabilize variance
    log_counts = np.log1p(normalized_counts)
    
    # PCA expects samples x genes
    pca = PCA(n_components=2)
    components = pca.fit_transform(log_counts.T)
    
    plot_df = pd.DataFrame({
        "PC1": components[:, 0],
        "PC2": components[:, 1],
        "Sample": log_counts.columns,
        "Condition": metadata_df.loc[log_counts.columns, condition_col].values
    })
    
    variance = pca.explained_variance_ratio_
    
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=plot_df, x="PC1", y="PC2", hue="Condition", s=100)
    plt.title("PCA of Normalized Counts")
    plt.xlabel(f"PC1 ({variance[0]:.1%} variance)")
    plt.ylabel(f"PC2 ({variance[1]:.1%} variance)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_volcano(results_df: pd.DataFrame, fdr_thresh: float, log2fc_thresh: float, output_path: str):
    """
    Plot a volcano plot highlighting significant genes.
    """
    plot_df = results_df.copy()
    
    # Calculate -log10 p-value
    # handle zeros or extremely small p-values to avoid inf
    min_pval = plot_df[plot_df["padj"] > 0]["padj"].min()
    if pd.isna(min_pval):
        min_pval = 1e-300
    plot_df["padj"] = plot_df["padj"].fillna(1)
    plot_df["-log10 padj"] = -np.log10(np.maximum(plot_df["padj"], min_pval * 0.1))
    
    # Categorize genes
    plot_df["Status"] = "Not Significant"
    sig_mask = (plot_df["padj"] < fdr_thresh) & (plot_df["log2FoldChange"].abs() >= log2fc_thresh)
    plot_df.loc[sig_mask & (plot_df["log2FoldChange"] > 0), "Status"] = "Up"
    plot_df.loc[sig_mask & (plot_df["log2FoldChange"] < 0), "Status"] = "Down"
    
    palette = {"Up": "#e41a1c", "Down": "#377eb8", "Not Significant": "#999999"}
    
    plt.figure(figsize=(8, 8))
    sns.scatterplot(
        data=plot_df, 
        x="log2FoldChange", 
        y="-log10 padj", 
        hue="Status", 
        palette=palette, 
        alpha=0.6,
        s=30,
        edgecolor=None
    )
    
    plt.axhline(-np.log10(fdr_thresh), color="k", linestyle="--", linewidth=1, alpha=0.5)
    plt.axvline(log2fc_thresh, color="k", linestyle="--", linewidth=1, alpha=0.5)
    plt.axvline(-log2fc_thresh, color="k", linestyle="--", linewidth=1, alpha=0.5)
    
    plt.title("Volcano Plot")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
