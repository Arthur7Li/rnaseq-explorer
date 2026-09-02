# RNA-seq Explorer

RNA-seq Explorer is a reproducible, configuration-driven toolkit for exploratory bulk RNA-seq differential-expression analysis.

**⚠️ Non-Clinical Use Only**: This tool is explicitly non-clinical, non-diagnostic, and intended for hypothesis-generation and educational use only. It must not be used for diagnostic or clinical conclusions.

## Quickstart (MVP Demo)

This quickstart uses the established [Airway demo dataset](data/airway/PROVENANCE.md) to demonstrate the complete end-to-end pipeline.

### Prerequisites
- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/) installed.

### 1. Acquire Demo Data
Run the following script to securely download the Airway demo dataset.
```bash
uv run python scripts/acquire_airway.py
```
This generates `data/airway/counts.csv` and `data/airway/metadata.csv`.

### 2. Run the Analysis
Run the pipeline using the demo configuration.
```bash
uv run rnax analyze --config config/airway.yaml
```

### 3. Review the Report
The pipeline will perform PyDESeq2 differential expression testing, extract significant hits, draw QC plots, and generate a final report.
Open the generated report in your browser:
```bash
open results/airway/report.html
```

## Features
- **Strict Data Validation**: Utilizes `pandera` to explicitly reject normalized inputs and ensure metadata mappings perfectly align.
- **Robust Statistics**: Incorporates `pydeseq2` for native Python standard Wald tests, removing external R dependencies.
- **Automated Reporting**: Produces Jinja2 static HTML reports along with publication-ready Volcano, PCA, and Library Size plots.

## Project Guardrails
Please see [AGENTS.md](AGENTS.md) and `.agent/GUARDRAILS.md` for strict data handling and operational constraints. No raw FASTQ processing, FPKM manipulation, or uncontrolled data commits are permitted in this repository.
