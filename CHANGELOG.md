# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-03
### Added
- **Snakemake Workflow Orchestration (Phase 5)**: Step-by-step resumption and explicit DAG definitions for all pipeline components.
- **Docker Containerization (Phase 6)**: Highly reproducible execution via `docker compose` using multi-stage `python:3.12-slim` builds.
- **Golden-File Snapshot Testing (Phase 7)**: Deterministic pipeline locking to ensure schema, artifact shape, and report structure never regress.
- **Performance Benchmarking (Phase 8)**: Synthetic data generator profiling up to 50,000 genes to provide explicit resource bounds.
- Full `CITATION.cff` and robust release documentation.
- Automated GitHub Actions release workflows to package execution artifacts.

## [0.2.0] - 2026-09-02
### Added
- **Complex Experimental Designs (Phase 2)**: Added support for paired samples, batch correction covariates, and multi-contrast processing.
- **Gene Ontology / Pathway Enrichment (Phase 3)**: Deep offline GSEA integration appending hyper-geometric pathway enrichment to outputs without mandatory network calls.
- **Parameter Sensitivity Analysis (Phase 4)**: Robustness metrics ensuring DE results aren't artifacts of arbitrary pre-filtering or threshold limits.
- **Interactive Scatter Plots (Phase 1)**: Integrated interactive Plotly visualizations inside the HTML report for deeper data exploration.

## [0.1.0] - 2026-08-30
### Added
- **MVP Pipeline (Phase 1)**: Initial implementation of reproducible bulk RNA-seq differential-expression using `PyDESeq2`.
- Foundational standard reporting via `jinja2`.
- Standard QC plots (PCA, Heatmap, Volcano, MA, Sample Distances).
- Ingestion validation scripts handling raw integer counts matrices.
- Acquisition scripts for `pasilla`, `airway`, and `bottomly` benchmark datasets.
- Reproducibility tracking (`PROVENANCE.md` and SHA-256 manifests).
