# Dataset Plan

RNA-seq Explorer uses a phased dataset strategy. The repository contains only small, derived demo inputs after their provenance and reuse terms are documented. It never includes raw sequencing reads, patient-identifiable data, or large downloaded files. See [DATA_POLICY.md](DATA_POLICY.md) for the governing rules.

## Decision summary

| Phase | Dataset | Role | Status |
|---|---|---|---|
| MVP | Airway / Himes et al. (2014) | Official end-to-end demo | Required |
| Good Portfolio | Bottomly et al. (2011) | Independent generalization and validation case | Required |
| Good Portfolio | Pasilla | Tiny deterministic test and tutorial fixture | Required |
| Outstanding | One curated GEO bulk-RNA-seq study | Real-world public-data case study | Conditional |

## Phase 1: Airway — MVP dataset

### Research question

**Which genes show treatment-associated expression differences between dexamethasone-treated and untreated human airway smooth-muscle cells, accounting for cell line?**

### Why this is the MVP

The Bioconductor `airway` experiment contains gene-level counts for four human airway smooth-muscle cell lines under untreated and dexamethasone-treated conditions. It is compact, biologically meaningful, and uses a paired design. It exercises the complete initial contract: raw counts, metadata, an explicit model, QC, results, and a reviewable report.

The associated GEO study is GSE52778. Its larger series includes untreated, dexamethasone, albuterol, and combined-treatment conditions. MVP deliberately supports only the eight-sample dexamethasone-versus-untreated subset.

### Required model

```text
expression ~ cell_line + treatment
contrast: dexamethasone - untreated
```

### Why it helps the project

| Advantages | Boundaries |
|---|---|
| Human cells, a clear treatment question, paired samples, and fast execution | Four cell lines means limited power |
| Supports metadata-aware design rather than a generic CSV-to-chart script | It is not a disease cohort and cannot justify clinical conclusions |
| Widely recognized workflow data make incorrect behavior easier to spot | Familiarity makes engineering—not biological novelty—the main portfolio signal |

### Required MVP artifacts

- `data/airway/counts.csv`: derived raw integer gene counts for the eight supported samples
- `data/airway/metadata.csv`: `sample_id`, `cell_line`, and `treatment`
- `data/airway/PROVENANCE.md`: source/version, subset rule, export command, checksums, and terms review
- `config/airway.yaml`: supported model and contrast
- `scripts/acquire_airway.R`: reproducible export with structure validation

### MVP acceptance evidence

- Eight samples, four cell lines, and both treatment levels are verified before analysis.
- Exported input is raw non-negative integer gene-level counts.
- The report states the model, contrast direction, source, and exploratory limitations.
- The tool does not use FPKM data as input to the count-based differential-expression path.
