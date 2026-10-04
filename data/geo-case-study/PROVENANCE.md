# GEO Case Study Provenance

## Source
- **Study:** Modelling mental disorders in zebrafish. Neurexins severely modulate anxiety, social behaviors and aggression.
- **GEO Accession:** [GSE324987](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE324987)
- **Publication:** PMID: 42362769
- **Organism:** Danio rerio (Zebrafish)

## Acquisition
- **Script:** `scripts/acquire_geo_case_study.py`
- **Retrieval Date:** 2026-10-03
- **Source URL:** `https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE324987&format=file&file=GSE324987%5Fraw%5Fcounts%2Ecsv%2Egz`
- **Preprocessing History:** 
  - The authors provided raw un-normalized gene-level integer counts.
  - The script extracts exactly 6 target samples: 3 Wild-Type controls (`WT-1_S1`, `WT-3_S2`, `WT-5_S3`) and 3 double-knockout mutants (`1a1bT-3_S7`, `1a1bT-4_S8`, `1a1bT-5_S9`).
  - Gene IDs are Ensembl Danio rerio IDs.
- **Reuse Terms:** Publicly available via NCBI GEO.

## Integrity
- `counts.csv` SHA-256: `ade1e4f9d3c0e062644635c83f200a239e6d5430ccc69b024e09fc0e3851fe1d`
- `metadata.csv` SHA-256: `5c68ff37bc09aff52d0918ac21fc56f8bbce3913842a6e945a39b8cadcf91267`
