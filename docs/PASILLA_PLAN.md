# Pasilla Test-Fixture Plan

## Role

Pasilla is the required **Good Portfolio** test and tutorial fixture. It is not the flagship biological demonstration; Airway remains the public-facing MVP.

## Why this dataset

The Bioconductor `pasilla` experiment-data package provides small gene/exon count data for a Drosophila RNAi experiment, including three knockdown and four control biological replicates. Its small size makes it well suited to fast, deterministic automated tests.

## What it verifies

- CLI execution from validated count and metadata inputs
- Two-condition design parsing
- Output-table schema and required result columns
- Deterministic report generation and snapshot/golden-file checks
- Safe errors for malformed counts, missing metadata, and unmatched sample IDs
- A short tutorial that does not require a large data download

## Required artifacts

- `data/pasilla/counts.csv`: a reviewed, permitted small gene-count fixture
- `data/pasilla/metadata.csv`: sample ID and knockdown/control condition
- `data/pasilla/PROVENANCE.md`: source package/version, terms, export process, sample map, and checksums
- `scripts/acquire_pasilla.R`: a reproducible acquisition/export helper
- Integration tests that produce and verify expected output structure

## Review gate

- [ ] Record installed package version, acquisition date, source terms, and export command.
- [ ] Verify the exact gene-count file and sample identifiers.
- [ ] Confirm three knockdown and four control biological replicates.
- [ ] Validate non-negative integer counts and unique gene/sample IDs.
- [ ] Keep only a small permitted fixture in Git; do not commit raw reads.
- [ ] Record SHA-256 checksums for committed derived files.

## Boundary

Pasilla's simpler unpaired design complements but does not replace Airway's paired cell-line design. A passing Pasilla test proves software behavior, not biological generality.

## Source

Brooks et al. (2011), *Conservation of an RNA regulatory map between Drosophila and mammals*, Genome Research; distributed through Bioconductor's `pasilla` experiment-data package.
