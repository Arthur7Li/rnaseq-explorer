from typing import Any, cast

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.spatial.distance import pdist, squareform
from scipy.stats import zscore
from sklearn.decomposition import PCA

# Colorblind-safe palette (Wong 2011)
CB_PALETTE = {
    "Up": "#D55E00",            # vermillion
    "Down": "#0072B2",          # blue
    "Not Significant": "#999999" # gray
}

# General colorblind-friendly discrete colors from Wong (2011)
WONG_PALETTE = [
    "#0072B2",  # blue
    "#D55E00",  # vermillion
    "#009E73",  # bluish green
    "#F0E442",  # yellow
    "#56B4E9",  # sky blue
    "#E69F00",  # orange
    "#CC79A7",  # reddish purple
]

PLOT_RC_PARAMS = {
    "axes.labelsize": 12,
    "axes.titlesize": 14,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
}


def plot_library_sizes(counts_df: pd.DataFrame, metadata_df: pd.DataFrame, condition_col: str, output_path: str) -> str:
    """
    Plot library sizes (total reads per sample).
    Returns descriptive alt text.
    """
    sizes = counts_df.sum(axis=0)
    plot_df = pd.DataFrame({
        "Sample": sizes.index,
        "Library Size": sizes.values,
        "Condition": metadata_df.loc[sizes.index, condition_col].values
    })
    
    unique_conditions = plot_df["Condition"].unique()
    palette = WONG_PALETTE[:len(unique_conditions)]
    
    with plt.rc_context(cast(Any, PLOT_RC_PARAMS)):
        plt.figure(figsize=(10, 6))
        sns.barplot(data=plot_df, x="Sample", y="Library Size", hue="Condition", dodge=False, palette=palette)
        plt.title("Library Sizes per Sample", fontsize=14)
        plt.xlabel("Sample", fontsize=12)
        plt.ylabel("Library Size", fontsize=12)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()
    
    alt_text = f"Bar chart showing total library sizes across {len(plot_df)} samples, colored by {condition_col}."
    return alt_text


def plot_pca(normalized_counts: pd.DataFrame, metadata_df: pd.DataFrame, condition_col: str, output_path: str) -> str:
    """
    Plot PCA of log1p transformed normalized counts.
    normalized_counts: genes x samples
    Returns descriptive alt text.
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
    unique_conditions = plot_df["Condition"].unique()
    palette = WONG_PALETTE[:len(unique_conditions)]
    
    with plt.rc_context(cast(Any, PLOT_RC_PARAMS)):
        plt.figure(figsize=(8, 6))
        sns.scatterplot(
            data=plot_df, 
            x="PC1", 
            y="PC2", 
            hue="Condition", 
            style="Condition", 
            s=100, 
            palette=palette
        )
        plt.title("PCA of Normalized Counts", fontsize=14)
        plt.xlabel(f"PC1 ({variance[0]:.1%} variance)", fontsize=12)
        plt.ylabel(f"PC2 ({variance[1]:.1%} variance)", fontsize=12)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()
    
    alt_text = (
        f"Principal component analysis scatter plot showing sample separation along "
        f"PC1 ({variance[0]:.1%} variance) and PC2 ({variance[1]:.1%} variance), "
        f"with colorblind-safe colors and distinct marker shapes for {condition_col}."
    )
    return alt_text


def plot_volcano(results_df: pd.DataFrame, fdr_thresh: float, log2fc_thresh: float, output_path: str) -> str:
    """
    Plot a volcano plot highlighting significant genes with colorblind-safe palette and marker shapes.
    Returns descriptive alt text.
    """
    plot_df = results_df.copy()
    
    # Calculate -log10 p-value
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
    
    markers = {"Up": "^", "Down": "v", "Not Significant": "o"}
    
    n_up = int((plot_df["Status"] == "Up").sum())
    n_down = int((plot_df["Status"] == "Down").sum())
    
    with plt.rc_context(cast(Any, PLOT_RC_PARAMS)):
        plt.figure(figsize=(8, 8))
        sns.scatterplot(
            data=plot_df, 
            x="log2FoldChange", 
            y="-log10 padj", 
            hue="Status", 
            style="Status",
            markers=markers,
            palette=CB_PALETTE, 
            alpha=0.6,
            s=35,
            edgecolor=None
        )
        
        plt.axhline(-np.log10(fdr_thresh), color="k", linestyle="--", linewidth=1, alpha=0.5)
        plt.axvline(log2fc_thresh, color="k", linestyle="--", linewidth=1, alpha=0.5)
        plt.axvline(-log2fc_thresh, color="k", linestyle="--", linewidth=1, alpha=0.5)
        
        plt.title("Volcano Plot", fontsize=14)
        plt.xlabel("log2FoldChange", fontsize=12)
        plt.ylabel("-log10 padj", fontsize=12)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()
    
    alt_text = (
        f"Volcano plot displaying log2 fold change against -log10 adjusted p-value. "
        f"{n_up} upregulated genes are highlighted in vermillion triangles and {n_down} "
        f"downregulated genes in blue inverted triangles at FDR < {fdr_thresh} and |log2FC| >= {log2fc_thresh}."
    )
    return alt_text


def plot_sample_distances(normalized_counts: pd.DataFrame, metadata_df: pd.DataFrame, condition_col: str, block_col: str | None, output_path: str) -> str:
    """
    Plot Sample Distance Matrix (Euclidean, log1p-normalized).
    Returns descriptive alt text.
    """
    log_counts = np.log1p(normalized_counts)
    
    # Pairwise Euclidean distances between samples
    distances = pdist(log_counts.T, metric="euclidean")
    dist_matrix = pd.DataFrame(
        squareform(distances),
        index=log_counts.columns,
        columns=log_counts.columns
    )
    
    # Annotations with colorblind-friendly colors
    col_colors = None
    if condition_col in metadata_df.columns:
        conditions = metadata_df.loc[log_counts.columns, condition_col]
        unique_conds = conditions.unique()
        lut = dict(zip(unique_conds, WONG_PALETTE[:len(unique_conds)]))
        col_colors = conditions.map(lut)
        
        if block_col and block_col in metadata_df.columns:
            blocks = metadata_df.loc[log_counts.columns, block_col]
            unique_blocks = blocks.unique()
            lut_block = dict(zip(unique_blocks, WONG_PALETTE[len(unique_conds):len(unique_conds) + len(unique_blocks)]))
            block_colors = blocks.map(lut_block)
            col_colors = pd.DataFrame({"Condition": col_colors, "Block": block_colors})
        else:
            col_colors = pd.DataFrame({"Condition": col_colors})

    with plt.rc_context(cast(Any, PLOT_RC_PARAMS)):
        g = sns.clustermap(
            dist_matrix,
            cmap="mako_r",
            col_colors=col_colors,
            row_cluster=True,
            col_cluster=True,
            figsize=(8, 8)
        )
        g.fig.suptitle("Sample Distance Matrix (Euclidean, log1p-normalized)", y=1.05, fontsize=14)
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
    
    alt_text = f"Hierarchical clustering heatmap of pairwise Euclidean sample distances across {len(dist_matrix)} samples based on log1p normalized counts."
    return alt_text


def plot_ma(results_df: pd.DataFrame, fdr_thresh: float, log2fc_thresh: float, output_path: str) -> str:
    """
    Plot an MA plot highlighting significant genes with colorblind-safe palette and marker shapes.
    Returns descriptive alt text.
    """
    plot_df = results_df.copy()
    
    plot_df["Status"] = "Not Significant"
    sig_mask = (plot_df["padj"] < fdr_thresh) & (plot_df["log2FoldChange"].abs() >= log2fc_thresh)
    plot_df.loc[sig_mask & (plot_df["log2FoldChange"] > 0), "Status"] = "Up"
    plot_df.loc[sig_mask & (plot_df["log2FoldChange"] < 0), "Status"] = "Down"
    
    markers = {"Up": "^", "Down": "v", "Not Significant": "o"}
    n_up = int((plot_df["Status"] == "Up").sum())
    n_down = int((plot_df["Status"] == "Down").sum())
    
    # x-axis is log10(baseMean)
    # add small pseudocount to avoid log10(0)
    plot_df["log10_baseMean"] = np.log10(plot_df["baseMean"] + 1e-1)
    
    with plt.rc_context(cast(Any, PLOT_RC_PARAMS)):
        plt.figure(figsize=(8, 6))
        sns.scatterplot(
            data=plot_df,
            x="log10_baseMean",
            y="log2FoldChange",
            hue="Status",
            style="Status",
            markers=markers,
            palette=CB_PALETTE,
            alpha=0.6,
            s=35,
            edgecolor=None
        )
        
        plt.axhline(0, color="k", linestyle="-", linewidth=1)
        plt.title("MA Plot", fontsize=14)
        plt.xlabel("Mean Normalized Count (log₁₀)", fontsize=12)
        plt.ylabel("log2FoldChange", fontsize=12)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()
    
    alt_text = (
        f"MA plot showing mean normalized count (log10) versus log2 fold change. "
        f"{n_up} upregulated genes shown as vermillion triangles, {n_down} downregulated genes "
        f"as blue inverted triangles, and non-significant genes as gray circles."
    )
    return alt_text


def plot_top_genes_heatmap(normalized_counts: pd.DataFrame, results_df: pd.DataFrame, metadata_df: pd.DataFrame, condition_col: str, block_col: str | None, n_top: int, output_path: str) -> str:
    """
    Plot a heatmap of the top n_top differentially expressed genes.
    Returns descriptive alt text.
    """
    # Sort by padj ascending, exclude NaN
    valid_res = results_df.dropna(subset=["padj"])
    top_genes = valid_res.sort_values("padj").head(n_top).index
    
    # Subset normalized counts
    subset_counts = normalized_counts.loc[top_genes]
    
    # Z-score each gene across samples
    z_scores_array = zscore(subset_counts.values, axis=1, nan_policy='omit')
    z_scores = pd.DataFrame(
        z_scores_array,
        index=subset_counts.index,
        columns=subset_counts.columns
    )
    # Fill any NaNs with 0 (e.g. if a gene has constant expression)
    z_scores = z_scores.fillna(0)
    
    # Sort columns by condition for readability
    sorted_samples = metadata_df.sort_values(by=condition_col).index
    # keep only samples that are in normalized_counts
    sorted_samples = [s for s in sorted_samples if s in z_scores.columns]
    z_scores = z_scores[sorted_samples]
    
    # Annotations with colorblind-friendly colors
    col_colors = None
    if condition_col in metadata_df.columns:
        conditions = metadata_df.loc[sorted_samples, condition_col]
        unique_conds = conditions.unique()
        lut = dict(zip(unique_conds, WONG_PALETTE[:len(unique_conds)]))
        col_colors = conditions.map(lut)
        
        if block_col and block_col in metadata_df.columns:
            blocks = metadata_df.loc[sorted_samples, block_col]
            unique_blocks = blocks.unique()
            lut_block = dict(zip(unique_blocks, WONG_PALETTE[len(unique_conds):len(unique_conds) + len(unique_blocks)]))
            block_colors = blocks.map(lut_block)
            col_colors = pd.DataFrame({"Condition": col_colors, "Block": block_colors})
        else:
            col_colors = pd.DataFrame({"Condition": col_colors})
            
    n_actual = len(top_genes)
    
    with plt.rc_context(cast(Any, PLOT_RC_PARAMS)):
        g = sns.clustermap(
            z_scores,
            cmap="vlag",
            center=0,
            col_colors=col_colors,
            row_cluster=True,
            col_cluster=False, # Keep columns ordered by condition
            figsize=(8, max(6, n_actual * 0.25))
        )
        g.fig.suptitle(f"Top {n_actual} DE Genes (Z-scored expression)", y=1.05, fontsize=14)
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
    
    alt_text = f"Z-score normalized expression clustered heatmap of the top {n_actual} differentially expressed genes across samples."
    return alt_text
