# Airway Dataset Provenance

- **Dataset Name**: Airway
- **Project Role**: MVP end-to-end demo dataset
- **Original Study Citation**: Himes BE, Jiang X, Wagner P, Hu R, Wang Q, Klanderman B, Whitaker RM, Duan Q, Lasky-Su J, Nikolos C, Jester W, Johnson M, Panettieri RA Jr, Tantisira KG, Weiss ST, Lu Q. "RNA-Seq transcriptome profiling identifies CRISPLD2 as a glucocorticoid responsive gene that modulates cytokine function in airway smooth muscle cells." *PLoS One*. 2014 Jun 13;9(6):e99625.
- **Stable Source / Accession**: GEO Accession GSE52778. Data sourced from Bioconductor `airway` package demonstrations.
- **Acquisition Date**: September 1, 2026
- **Data Source**: Bioconductor Workshops GitHub repository
- **Acquisition Command**: `uv run python scripts/acquire_airway.py`
- **Original Data Type**: RNA-Seq gene-level read counts
- **Preprocessing History**: Counts were extracted from the Bioconductor `airway` package SummarizedExperiment object.
- **Inclusion / Exclusion Rule**: Only the 8 samples comparing untreated vs dexamethasone treatments across 4 cell lines were included, matching the exact MVP paired design.
- **Terms / License Review**: Open research data (GEO). Standard scientific redistribution is permitted for tutorial and reproducible research purposes.
- **Known Limitations**: This is a small in vitro experiment containing 4 biological replicates. It provides a robust technical pipeline test but lacks the power for complex trait inference or clinical associations.

## Checksums

```text
06d2167e72a2c0e9143f8b7f7ea9022208584e1cf3907094ca13d798237eb0d9  data/airway/counts.csv
a8eb69074aa542628d011993afd4410105a5e417f1d5a87d40b8ad7739815de5  data/airway/metadata.csv
```
