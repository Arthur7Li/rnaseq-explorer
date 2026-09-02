# Airway Dataset Provenance

## Project role

Official MVP end-to-end demonstration: exploratory differential-expression analysis of dexamethasone-treated versus untreated human airway smooth-muscle cells, accounting for matched cell line.

## Original study and sources

- Himes et al. (2014), *RNA-Seq Transcriptome Profiling Identifies CRISPLD2 as a Glucocorticoid Responsive Gene that Modulates Cytokine Function in Airway Smooth Muscle Cells*, PLOS ONE 9(6):e99625. PMID: 24926665.
- GEO accession: GSE52778.
- Derived count/metadata source: Bioconductor `airway` experiment-data package.

## Inclusion rule

Use the eight samples in the `airway` package: four airway smooth-muscle cell lines, each represented in untreated and dexamethasone-treated conditions. Exclude the albuterol and combined-treatment samples available in the broader GEO series because they are outside the MVP's supported two-condition scope.

## Derived-file contract

- `counts.csv`: raw, non-negative integer, gene-level counts; one unique `gene_id` column and eight unique sample columns.
- `metadata.csv`: exactly eight rows containing `sample_id`, `cell_line`, and `treatment`.
- `treatment` values: `untreated` and `dexamethasone`.
- Analysis model: `expression ~ cell_line + treatment`; contrast: dexamethasone minus untreated.

## Acquisition

Run from the repository root:

```bash
Rscript scripts/acquire_airway.R
```

The script validates package structure, count type, sample count, condition levels, and identifier uniqueness before exporting files. It also writes `acquisition-sessionInfo.txt`.

## Completion checklist before committing derived inputs

- [ ] Record acquisition date.
- [ ] Record installed `airway` and Bioconductor versions.
- [ ] Review source-package and original-study reuse terms; record the redistribution decision.
- [ ] Record gene-ID/annotation details provided by the package.
- [ ] Confirm the final sample map has four cell lines and two samples per cell line.
- [ ] Verify that all counts are raw non-negative integers.
- [ ] Compute and record SHA-256 checksums for `counts.csv` and `metadata.csv`.
- [ ] Record the acquisition script commit SHA.

## Interpretation boundary

This is an exploratory research and teaching dataset. Differential expression in this analysis does not establish causation, clinical efficacy, diagnosis, treatment guidance, or validated biomarkers.
