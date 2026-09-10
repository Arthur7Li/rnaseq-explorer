# Pasilla Dataset Provenance

## Source Information
- **Name:** pasilla (Bioconductor Data Package)
- **Version:** 1.40.0
- **URL:** [Bioconductor pasilla](https://bioconductor.org/packages/release/data/experiment/html/pasilla.html)
- **Archive URL:** `https://bioconductor.org/packages/release/data/experiment/src/contrib/pasilla_1.40.0.tar.gz`
- **Citation:** Brooks AN, Yang L, Duff MO, Hansen KD et al. Conservation of an RNA regulatory map between Drosophila and mammals. Genome Res 2011 Feb;21(2):193-202. PMID: 20921232

## Data Policy Compliance
This dataset is a widely used, publicly available research dataset specifically designed for benchmarking differential expression tools (it is the standard vignette dataset for DESeq2).
- It contains no human subjects data.
- It contains no clinical, diagnostic, or proprietary information.
- It is freely redistributable for educational and testing purposes.

## Pre-processing and Mapping
The data was downloaded using the `scripts/acquire_pasilla.py` automation script.
1. `pasilla_gene_counts.tsv` was extracted, formatted as CSV, and saved as `counts.csv`.
2. `pasilla_sample_annotation.csv` was extracted.
3. The sample IDs in the annotation file (e.g., `untreated1fb`) were stripped of the `fb` suffix to map perfectly to the columns in `counts.csv` (e.g., `untreated1`).
4. Only the `sample_id` and `condition` columns were retained for testing a simple unpaired, single-factor experimental design.

## File Integrity Checksums
*Generated automatically by `scripts/acquire_pasilla.py`*

- **`counts.csv` SHA-256**: `ac6d11f37578e23da60f86e1a1f0aaebb8d3ffb5ceb0b9b8f9abe17a1a8f7aa7`
- **`metadata.csv` SHA-256**: `dfdc6b46ed698a3de38f7031d2baf79e27cdf7265fd49776f772bb6996e7dfad`
