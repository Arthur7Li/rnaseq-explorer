# RNA-seq Explorer Snakemake Workflow

While the direct CLI (`rnax analyze`) remains the primary interface for quick runs, power users can use Snakemake for a modular, step-wise Directed Acyclic Graph (DAG) execution.

## Installation

Snakemake is an optional dependency. Install it using:
```bash
uv pip install rnax[workflow]
# or
pip install snakemake>=8.0
```

## Running the Workflow

Execute the workflow by specifying your RNA-seq Explorer YAML configuration file:
```bash
snakemake -c1 -s workflow/Snakefile --config rnax_config=config/pasilla.yaml
```

## Workflow DAG

The pipeline is split into distinct rules, allowing independent execution and resumption:
1. `validate`: Validates inputs and creates a reproducibility manifest.
2. `deseq2`: Executes PyDESeq2 to fit models and generate differential expression results.
3. `plots`: Renders the PCA, Volcano, MA, and Distance Heatmap plots.
4. `sensitivity`: Tests FDR/log2FC thresholds to assign a Stability Verdict.
5. `annotate`: Performs offline Gene Set Enrichment (if enabled).
6. `report`: Renders the final HTML report from the gathered outputs.

## Failure Recovery

Snakemake automatically saves progress. If a rule fails, you only need to fix the issue and re-run the `snakemake` command to resume from where it left off.
- **If `validate` fails:** Check your `counts.csv` or `metadata.csv` formatting and re-run.
- **If `deseq2` fails:** Usually memory constraints or perfectly collinear conditions. Fix the design formula in the config.
- **If `annotate` fails:** Ensure the offline enrichment databases have been downloaded (via `scripts/fetch_annotations.py`).

