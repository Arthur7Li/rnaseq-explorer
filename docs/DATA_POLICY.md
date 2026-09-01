# Data Policy

## Purpose

This policy keeps RNA-seq Explorer reproducible, ethically cautious, and appropriate for a public source repository.

## Permitted repository data

Commit a derived dataset only when it is small and necessary for a demo or automated test, contains no personal or restricted information, has documented source and terms, meets the input contract, and has a checksum recorded in its provenance file.

## Never commit

- FASTQ, BAM, CRAM, or other raw sequencing/alignment files
- Controlled-access, credentialed, or data-use-agreement datasets
- Patient-identifiable data or sensitive free-text metadata
- Tokens, credentials, temporary download URLs, or private paths
- Matrices with uncertain provenance, transformation history, or sample identity

## Count-matrix contract

The initial differential-expression path accepts only raw, non-negative integer, gene-level counts. TPM, FPKM, RPKM, CPM, percentages, log-transformed values, precomputed fold changes, and other normalized measures are not valid count-model inputs.

The first column is a unique gene identifier. Each remaining column is a unique sample ID. Metadata has exactly one row per sample, matches those IDs exactly, names the condition field, and includes every required design covariate.

## Provenance requirements

Every dataset folder must contain `PROVENANCE.md` with:

- Dataset name and project role
- Original study citation and stable source/accession
- Acquisition date, data source, package/database version, and acquisition command
- Original data type, annotation/gene-ID version, and preprocessing history
- Inclusion/exclusion rule and final sample mapping
- Terms/license review and redistribution decision
- SHA-256 checksums for committed derived files
- Known limitations and assumptions

## Release gate

No dataset becomes a release input until its count type, sample-to-metadata mapping, documentation, terms, and checksums have been verified independently.
