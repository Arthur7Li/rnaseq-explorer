# RNA-seq Explorer

> From validated count matrices to reviewable biological hypotheses.

RNA-seq Explorer is a reproducible, configuration-driven toolkit for exploratory **bulk RNA-seq differential-expression analysis** of small research and teaching datasets. It validates inputs, records provenance and analysis settings, runs transparent quality-control and differential-expression steps, and produces a shareable HTML report.

## The pitch

RNA-seq experiments can measure expression for thousands of genes at once, but a count table and a spreadsheet of sample labels are not an answer. Analysis is vulnerable to sample/metadata mismatches, low-count noise, uneven library sizes, outliers, batch effects, undisclosed choices, and false positives from testing thousands of genes.

RNA-seq Explorer makes the first-pass downstream analysis structured and auditable. Given gene-level **raw integer counts** plus sample metadata, it answers: **which genes differ between specified conditions, how strong is the evidence, which samples merit investigation, and exactly how can the analysis be reproduced?**

It is a research- and teaching-support tool for generating hypotheses. It is **not** diagnostic software, a clinical decision system, a causal-inference engine, or a replacement for expert bioinformatics review.

## What it helps with

| Problem | Project response | Practical benefit |
|---|---|---|
| Counts and metadata are hard to trust | Validate sample IDs, duplicates, missing values, design fields, count types, and zero-heavy genes | Catches preventable errors before statistical analysis |
| Quality problems are hidden | Library-size summaries, PCA, clustering, and transparent outlier warnings | Makes unexpected grouping and potential batch effects visible |
| Thousands of tests invite misleading hits | Filter low-information genes; use a documented model and false-discovery-rate adjusted results | Produces a defensible, prioritized hypothesis list |
| Results are ad hoc notebooks | Save config, input hashes, package versions, commands, and outputs in a report | A collaborator can review or rerun the analysis |
| Biological results are difficult to communicate | Produce tables and interpretable QC/result figures | Gives students and labs a clear artifact for discussion |

## Core use cases

1. **Disease or phenotype exploration.** Compare control and condition samples to identify candidate expression changes and pathway-level hypotheses.
2. **Drug-response exploration.** Compare treated and untreated samples to describe transcriptional responses and candidate response signatures.
3. **Research QA.** Create a standardized first-pass report before a lab meeting, paper figure draft, or handoff to a bioinformatician.
4. **Teaching.** Give students a visible, reproducible workflow for learning metadata validation, normalization, PCA, multiple testing, and careful interpretation.
5. **Public-data reanalysis.** Reproduce a documented baseline analysis on a small, appropriately licensed public count dataset.

## Intended audience

- Undergraduate and graduate learners in computational biology, genetics, statistics, and bioinformatics
- Research assistants and wet-lab teams needing a transparent first-pass analysis
- Computational-biology labs and core facilities evaluating reproducibility and usability
- Biotech, pharma, health-data, and research-software hiring teams evaluating engineering judgment
- Open-source contributors who value documented inputs, tests, repeatable environments, and clear limitations

## Product boundary

### Version 1 does

- Analyze **bulk, gene-level count matrices** with a small two-condition study design
- Accept a sample-metadata table and a configuration file
- Validate inputs and create QC/result figures
- Run a documented differential-expression method and report adjusted p-values
- Save a reproducible analysis record and HTML report

### Version 1 does not

- Download or process raw FASTQ reads, align reads, or quantify transcripts
- Support single-cell RNA-seq, every experimental design, or clinical workflows
- Claim biomarker discovery, diagnosis, treatment recommendation, causation, or biological validation
- Hide important modeling decisions behind a one-click black box

## Example workflow

Install dependencies using [uv](https://github.com/astral-sh/uv):

```bash
uv sync
```

Run the pipeline:

```bash
uv run rnax analyze \
  --counts data/counts.csv \
  --metadata data/metadata.csv \
  --config config/analysis.yaml \
  --output results/demo
```

Expected deliverables include an input-validation summary, sample-QC figures, PCA, a differential-expression table with log2 fold changes and adjusted p-values, a volcano plot, a top-gene heatmap, and a reproducibility manifest.

## Status

**Planning / repository initialization.** The scope, release gates, and acceptance criteria are in [docs/ROADMAP.md](docs/ROADMAP.md). The durable product rationale is in [docs/VISION.md](docs/VISION.md).

## Development principles

- Make every result traceable to an input, configuration, software environment, and command.
- Prefer a small validated workflow over unsupported feature breadth.
- Fail clearly on invalid inputs; never silently coerce or discard data.
- Separate exploratory notebooks from the production pipeline.
- Keep biological and statistical limitations close to the reported results.
- Write tests before calling a feature complete.

## Planned stack

Python will own the command-line interface, validation, orchestration, figures, and reporting. Differential-expression support will initially be selected after a reproducibility spike; candidates include a documented Python implementation or an isolated R/DESeq2 backend. The choice must preserve raw-count assumptions, deterministic execution, testability, and a straightforward local installation.

## Repository map

```text
docs/          vision, roadmap, data policy, methods, limitations
config/        example analysis configurations
data/demo/     small permitted demonstration inputs only
src/           package source
tests/         automated tests
notebooks/     non-production exploration only
results/       generated outputs; normally gitignored
```

## Contributing

This repository is initially a learning and portfolio project. Contributions and issue reports will be welcome once the MVP interface and data policy are stable. See [CONTRIBUTING.md](CONTRIBUTING.md).
