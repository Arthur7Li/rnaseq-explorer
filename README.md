# RNA-seq Explorer

![CI](https://github.com/Arthur7Li/rnaseq-explorer/actions/workflows/ci.yml/badge.svg)

RNA-seq Explorer is a reproducible, configuration-driven toolkit for exploratory bulk RNA-seq differential-expression analysis. Designed for small research and teaching datasets, it provides a transparent, end-to-end pipeline from validated count matrices to fully auditable, static HTML reports.

> [!WARNING]
> **Non-Clinical, Hypothesis-Generating Use Only**  
> RNA-seq Explorer is strictly intended for scientific exploration, teaching, and hypothesis generation. It is **not** clinical software, does not provide diagnostic conclusions, and cannot establish biomarker validity or therapeutic causation. All candidate genes require independent experimental validation.

---

## Quickstart

Run a complete analysis in under two minutes using the bundled [Pasilla demo fixture](data/pasilla/PROVENANCE.md):

### Prerequisites
- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/) package manager

### 1. Clone & Install
```bash
git clone https://github.com/Arthur7Li/rnaseq-explorer.git
cd rnaseq-explorer
uv sync
```

### 2. Run Analysis
```bash
uv run rnax analyze --config config/pasilla.yaml
```

### 3. Inspect Results
Open the generated interactive HTML report in any web browser:
```bash
open results/pasilla/report.html
```

---

## Container Execution (Docker)

RNA-seq Explorer can be run natively via `uv` (as shown above) or within an isolated Docker container to guarantee environment reproducibility across different operating systems.

### Option 1: Docker Compose (Recommended)
We provide a `docker-compose.yml` that automatically handles volume mounts for your `config`, `data`, and `results` directories.

```bash
# Build the image and run the pasilla analysis
docker compose run --rm rnax analyze --config config/pasilla.yaml
```

### Option 2: Docker CLI
If you prefer raw Docker commands, you must manually mount your local directories:

```bash
# Build the image
docker build -t rnax .

# Run the container with volume mounts
docker run --rm \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/results:/app/results \
  rnax analyze --config config/pasilla.yaml
```

**Note:** Both the native `uv run rnax` route and the container route are fully supported and produce mathematically identical results.

---

## Supported Datasets

RNA-seq Explorer provides automated acquisition scripts and provenance logs for three benchmark datasets:

| Dataset | Organism | Samples | Design | Research Question | Config File |
|---|---|---|---|---|---|
| **Airway** | *Homo sapiens* | 8 (4 treated, 4 untreated) | Paired (blocking on cell line) | Effect of dexamethasone on airway smooth muscle cells | `config/airway.yaml` |
| **Pasilla** | *Drosophila melanogaster* | 7 (3 knockdown, 4 control) | Unpaired two-group | Transcriptional consequences of *pasilla* (splicing factor) RNAi | `config/pasilla.yaml` |
| **Bottomly** | *Mus musculus* | 10 (5 C57BL/6J, 5 DBA/2J) | Unpaired two-group | Baseline striatal gene expression differences across inbred mouse strains | `config/bottomly.yaml` |
| **Zebrafish** | *Danio rerio* | 6 (3 WT, 3 KO) | Unpaired two-group | Transcriptional consequences of neurexin-1 double-knockout | `config/geo-case-study.yaml` |

To acquire any dataset:
```bash
uv run python scripts/acquire_pasilla.py
uv run python scripts/acquire_airway.py
uv run python scripts/acquire_bottomly.py
uv run python scripts/acquire_geo_case_study.py
```

---

## Input Specification

RNA-seq Explorer requires two CSV files: a **counts matrix** and a **sample metadata table**.

### 1. Counts Matrix (`counts.csv`)
- **Format:** CSV with gene IDs as the first column and sample identifiers as subsequent column headers.
- **Values:** Raw, non-negative integer read counts.
- **Constraints:**
  - Float values, normalized values (FPKM, RPKM, TPM), and log-transformed counts are **strictly rejected**.
  - No missing (`NaN` / null) values allowed.
  - All sample column headers must match entries in the metadata `sample_id` column.

Example:
```csv
gene_id,sample_1,sample_2,sample_3,sample_4
FBgn0000008,92,161,76,70
FBgn0000014,5,1,0,0
FBgn0000017,4356,4120,3980,4210
```

### 2. Sample Metadata (`metadata.csv`)
- **Format:** CSV with at least two columns: `sample_id` and the biological condition.
- **Constraints:**
  - `sample_id` must match columns in `counts.csv` exactly.
  - The condition column must contain **exactly two distinct levels** (e.g., `control` vs `treated`).
  - An optional blocking covariate column can be specified for paired or batch-corrected designs.

Example:
```csv
sample_id,condition,batch
sample_1,untreated,batch_1
sample_2,untreated,batch_2
sample_3,treated,batch_1
sample_4,treated,batch_2
```

---

## Pipeline Outputs

Every run produces a structured, self-contained output directory:

```
results/pasilla/
├── report.html             # Static, standalone HTML report with embedded figures and provenance
├── results.csv             # Full differential expression statistics table
├── normalized_counts.csv   # Median-of-ratios normalized count matrix
├── library_sizes.png       # QC: Total read counts per sample library
├── pca.png                 # QC: Principal Component Analysis (log1p normalized counts)
├── sample_distances.png    # QC: Hierarchical clustering of Euclidean sample distances
├── volcano.png             # DE: Volcano plot of effect size vs statistical significance
├── ma_plot.png             # DE: Log fold change vs mean normalized count
└── top_genes_heatmap.png   # DE: Clustered heatmap of top N significant genes (Z-scored)
```

### Differential Expression Table (`results.csv`)
Contains standard PyDESeq2 statistical metrics:
- `baseMean`: Mean of normalized counts across all samples.
- `log2FoldChange`: Effect size estimate (log₂ fold change between comparison and reference).
- `lfcSE`: Standard error of the log₂ fold change estimate.
- `stat`: Wald statistic.
- `pvalue`: Wald test p-value.
- `padj`: Benjamini-Hochberg False Discovery Rate (FDR) adjusted p-value.

---

## Methodology Overview

RNA-seq Explorer uses established, standard statistical methodologies implemented via [PyDESeq2](https://github.com/owkin/PyDESeq2):

1. **Low-Count Filtering**: Eliminates uninformative low-count genes prior to analysis (default: &ge; 10 counts in &ge; 2 samples).
2. **Normalization**: Computes sample-specific size factors using the **median-of-ratios** method (Anders & Huber, 2010) to account for sequencing depth and library composition biases.
3. **Dispersion Estimation**: Fits gene-wise dispersion estimates using maximum likelihood, models the mean-dispersion relationship across all genes, and shrinks dispersions toward the trend via empirical Bayes estimation.
4. **Generalized Linear Model (GLM)**: Fits negative binomial GLMs for each gene:
   $$\log_2(q_{ij}) = x_i^T \beta_j$$
5. **Hypothesis Testing**: Performs two-sided **Wald tests** on coefficients of interest.
6. **Multiple Testing Correction**: Applies the **Benjamini-Hochberg (FDR)** procedure to control false discoveries.

---

## Filtering Defaults & Customization

Pre-filtering thresholds can be customized in your YAML configuration:

```yaml
filtering:
  minimum_count: 10      # Minimum count required per sample
  minimum_samples: 2     # Minimum number of samples meeting minimum_count
```

All pre-filtering statistics (genes before, genes after, genes dropped) are logged during analysis and recorded transparently in the HTML report.

---

## Limitations

- **Exploratory Scope**: Designed for hypothesis generation; not suitable for medical diagnosis or clinical decision-making.
- **Count-Level Only**: Operates exclusively on gene-level count matrices; does not perform raw read alignment, transcript assembly, or isoform quantification.
- **Sample Size Constraints**: Bulk RNA-seq with low replicate counts ($n \le 3$ per group) has limited power; negative results do not demonstrate absence of effect.
- **Correlation vs. Causation**: Statistical association between condition and gene expression does not establish molecular mechanism or causality.

---

## Citations & Attribution

When using RNA-seq Explorer or its bundled datasets, please cite:

- **PyDESeq2**: Muzellec, B., Teleńczuk, M., Cvetkovic, N., & Keggl, B. (2023). PyDESeq2: a python package for bulk RNA-seq differential expression analysis. *Bioinformatics*, 39(10), btad547.
- **DESeq2**: Love, M. I., Huber, W., & Anders, S. (2014). Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2. *Genome Biology*, 15(12), 550.
- **Airway Dataset**: Himes, B. E. et al. (2014). RNA-Seq transcriptome profiling identifies CRISPLD2 as a glucocorticoid responsive gene that modulates cytokine function in airway smooth muscle cells. *PLoS ONE*, 9(6), e99625.
- **Pasilla Dataset**: Brooks, A. N. et al. (2011). Conservation of an RNA regulatory map between *Drosophila* and mammals. *Genome Research*, 21(2), 193–202.
- **Bottomly Dataset**: Bottomly, D. et al. (2011). Evaluating gene expression in C57BL/6J and DBA/2J mouse striatum using RNA-Seq and microarrays. *PLoS ONE*, 6(3), e17820.
- **Zebrafish Dataset**: Elegheert, J. et al. (2026). Modelling mental disorders in zebrafish. Neurexins severely modulate anxiety, social behaviors and aggression. *[GEO: GSE324987]*

---

## License & Contributing

- **License:** [MIT License](LICENSE)
- **Contributing:** Please see [CONTRIBUTING.md](CONTRIBUTING.md) and our [Code of Conduct](CODE_OF_CONDUCT.md).
- **Agentic Guardrails:** Mandatory instructions and operating boundaries for autonomous agents are detailed in [AGENTS.md](AGENTS.md) and `.agent/GUARDRAILS.md`.
