# Annotation Data Provenance

The gene annotations bundled in this directory are intended for reproducible, offline exploratory analysis. 

- `human_genes.csv`
- `mouse_genes.csv`
- `drosophila_genes.csv`

**Source:** Ensembl BioMart (Mocked for MVP)
**Date Retrieved:** 2026-09-30
**Version:** Ensembl Release 110 (simulated)

To update these annotations, run:
```bash
python scripts/fetch_annotations.py
```
*Note: The fetch script requires network access.*
