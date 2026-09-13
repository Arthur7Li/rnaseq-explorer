# Guided Walkthrough: Pasilla Differential Expression Analysis

This walkthrough guides you through a complete, reproducible bulk RNA-seq differential expression analysis using RNA-seq Explorer and the bundled [Pasilla demo dataset](../data/pasilla/PROVENANCE.md).

Total time: **~2 minutes**.

> [!NOTE]
> A live terminal recording (`asciinema`) demonstrating this exact workflow is available in the project releases.

---

## Step 1: Environment Setup

Clone the repository and install dependencies with `uv`:

```bash
git clone https://github.com/Arthur7Li/rnaseq-explorer.git
cd rnaseq-explorer
uv sync
```

Verify that the CLI is ready:

```bash
uv run rnax --help
```

Expected output:
```text
Usage: rnax [OPTIONS] COMMAND [ARGS]...

  RNA-seq Explorer CLI.

Options:
  --help  Show this message and exit.

Commands:
  analyze  Run the differential expression analysis pipeline.
```

---

## Step 2: Acquire Fixture Data

The repository includes a pure-Python downloader for the Drosophila *pasilla* RNAi dataset (Brooks et al., 2011). Run:

```bash
uv run python scripts/acquire_pasilla.py
```

Expected output:
```text
INFO: Downloading Bioconductor pasilla bundle from https://bioconductor.org/packages/release/data/experiment/src/contrib/pasilla_1.40.0.tar.gz
INFO: Extracting counts and metadata from tarball in memory...
INFO: Saved counts to data/pasilla/counts.csv (14599 genes, 7 samples)
INFO: Saved metadata to data/pasilla/metadata.csv (7 samples)
INFO: counts.csv SHA-256: ac6d11f37578e23da60f86e1a1f0aaebb8d3ffb5ceb0b9b8f9abe17a1a8f7aa7
INFO: metadata.csv SHA-256: dfdc6b46ed698a3de38f7031d2baf79e27cdf7265fd49776f772bb6996e7dfad
INFO: Pasilla dataset successfully acquired.
```

This ensures cryptographic integrity matches `data/pasilla/PROVENANCE.md`.

---

## Step 3: Run Differential Expression Analysis

Execute the end-to-end pipeline with the provided configuration:

```bash
uv run rnax analyze --config config/pasilla.yaml
```

The CLI performs the following automated steps:
1. **Config Validation**: Validates paths, factor levels, and threshold parameters.
2. **Data Integrity Check**: Verifies integer count values and ensures all 7 samples align between count matrix and metadata.
3. **Pre-filtering**: Drops genes with fewer than 10 counts in at least 2 samples (14,599 &rarr; 8,423 genes).
4. **PyDESeq2 GLM**: Estimates size factors, fits dispersions, and runs Wald significance tests.
5. **Report & Plot Generation**: Generates publication-ready figures, CSVs, and an interactive HTML report.

Expected output snippet:
```text
Successfully parsed configuration from config/pasilla.yaml
Successfully validated 14599 genes across 7 samples.
Running differential expression analysis...
Fitting size factors...
Fitting dispersions...
Fitting dispersion trend curve...
Fitting MAP dispersions...
Fitting LFCs...
Running Wald tests...
Log2 fold change & Wald test p-value: condition treated vs untreated
Generating report and plots...
Differential expression complete. 8423 genes analyzed.
Output saved to: results/pasilla
```

---

## Step 4: Inspect the Output Directory

All output files are located in `results/pasilla/`:

```bash
ls -l results/pasilla/
```

### Key Files Generated:

| Output File | Description | What to Look For |
|---|---|---|
| `report.html` | Interactive, static HTML report | Open in a browser to review the complete summary, QC plots, and reproducibility manifest. |
| `results.csv` | Full statistics table | Contains `baseMean`, `log2FoldChange`, `pvalue`, and `padj` for all 8,423 tested genes. |
| `normalized_counts.csv` | Normalized expression matrix | Size-factor adjusted counts for downstream exploratory analyses. |
| `library_sizes.png` | Library size QC | Bar chart confirming sequencing depth per sample library. |
| `pca.png` | Principal Component Analysis | Visual inspection of treated vs untreated sample separation along PC1 and PC2. |
| `sample_distances.png` | Clustered distance heatmap | Pairwise Euclidean distances confirming replicate consistency. |
| `volcano.png` | Volcano plot | Effect size vs FDR, highlighting candidate differential expression targets. |
| `ma_plot.png` | MA plot | Mean abundance vs log₂ fold change across all analyzed genes. |
| `top_genes_heatmap.png` | Clustered heatmap of top genes | Z-scored expression across samples for the top 30 significant genes. |

---

## Step 5: Open the HTML Report

View the rendered report:

```bash
open results/pasilla/report.html
# On Linux: xdg-open results/pasilla/report.html
```

Review the following structured sections:
1. **Analysis Metadata & Data Provenance**: Check input file SHA-256 hashes.
2. **QC Observations**: Review library size balances and replicate clustering patterns without making causal inferences.
3. **Statistical Methodology**: Details the negative binomial model and multiple testing corrections applied.
4. **Differential Expression**: Visualizes volcano and MA distributions alongside top candidate genes.
5. **Reproducibility Manifest**: Captures the exact CLI command, package versions, OS environment, and random seed.
