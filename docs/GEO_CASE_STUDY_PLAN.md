# GEO Case-Study Selection Gate

## Role

One curated public bulk-RNA-seq study is an **Outstanding-version** case study. It demonstrates public-data hygiene and responsible interpretation after Airway and Bottomly are reproducible. It is not selected yet.

## Goal

Show that RNA-seq Explorer can take a carefully audited public dataset from documented inputs to a reproducible, reviewable exploratory report. The goal is hypothesis generation—not diagnosis, treatment guidance, clinical validation, or causal claims.

## Selection requirements

A study is eligible only when all requirements below are satisfied:

1. It has a stable GEO accession and an associated peer-reviewed publication.
2. Raw gene-level non-negative integer counts are available directly or can be acquired reproducibly from a permitted public source.
3. Each comparison group has at least three biological replicates; five or more is preferred.
4. Condition labels and critical covariates are complete, consistent, and mapped to sample IDs.
5. Tissue/cell type, intervention or phenotype, and comparison direction can be stated in one clear sentence.
6. Source, retrieval date, reuse terms, annotation version, and preprocessing history can be recorded.
7. Its design is already supported, or required support is implemented and tested before the dataset is admitted.
8. The result report can state meaningful caveats without relying on diagnostic or causal language.

## Rejection criteria

Reject a candidate if it has only TPM/FPKM/log-normalized values; ambiguous or incomplete metadata; unavailable critical covariates; unclear reuse terms; fewer than three replicates per group; incompatible mixed tissues; unexplained batch differences; or a project story that requires a disease-diagnosis claim.

## Required deliverables after selection

- `data/geo-case-study/PROVENANCE.md` with full source, data, and processing record
- `config/geo-case-study.yaml` with a specific supported model and contrast
- A dataset selection decision record explaining why candidates passed or failed
- Input validation results, reproducibility manifest, and study-specific limitations in the report
- A statement that the analysis is exploratory and must be reviewed by qualified domain experts

## Sequencing rule

Do not download, analyze, or present a GEO case study as an official project example until Airway and Bottomly both run from a clean environment and meet their documented acceptance criteria.
