# Bottomly Validation Dataset Plan

## Role

Bottomly et al. is the required **Good Portfolio** validation dataset. It tests whether RNA-seq Explorer is a reusable, configuration-driven tool rather than a workflow hard-wired to the Airway demo.

## Research question

**Which genes show differential expression between C57BL/6J (B6) and DBA/2J (D2) mouse striatum samples in the Bottomly et al. experiment?**

## Dataset rationale

The experiment has 21 samples: 10 B6 and 11 D2. Compared with Airway, it contributes a larger cohort, different organism, and different biological setting. A successful analysis should preserve the same input-validation, QC, report, and reproducibility guarantees while using a dataset-specific configuration.

## Scientific boundary

This is a mouse-strain comparison, not a controlled intervention. The original study discusses possible strain-specific mapping/reference bias caused by sequence variation. RNA-seq Explorer consumes an existing count matrix and cannot correct unknown upstream alignment bias. Its report must name this limitation and avoid claiming simple causal strain effects.

## Required repository artifacts

- `data/bottomly/counts.csv`: reviewed gene-level raw integer counts
- `data/bottomly/metadata.csv`: reviewed sample IDs and strain labels
- `data/bottomly/PROVENANCE.md`: source, annotation, processing, terms, sample map, and checksums
- `config/bottomly.yaml`: B6/D2 design and contrast
- `docs/VALIDATION.md`: evidence that the pipeline runs on both Airway and Bottomly

## Data-readiness checklist

- [ ] A stable public source provides gene-level raw non-negative integer counts, not only normalized values or precomputed DE results.
- [ ] The original study and stable source/accession are recorded.
- [ ] Source terms and whether derived data may be redistributed are reviewed.
- [ ] Every count-matrix column maps to exactly one metadata row.
- [ ] Metadata contains exactly 10 B6 and 11 D2 samples.
- [ ] Gene identifiers are unique and annotation version is documented.
- [ ] Count values are validated as non-negative integers.
- [ ] Retrieval date, acquisition command, preprocessing history, sample inclusion/exclusion choices, and SHA-256 checksums are recorded.
- [ ] The report contains the strain-specific mapping-bias limitation.

## Success criteria

The Bottomly run is complete only when a fresh environment can produce the same report structure and result schema as Airway, all validation checks pass, and the README/validation document explains why biological result counts need not match between datasets.

## Source study

Bottomly et al. (2011), *Evaluating Gene Expression in C57BL/6J and DBA/2J Mouse Striatum Using RNA-Seq and Microarrays*, PLOS ONE 6(3):e17820. DOI: 10.1371/journal.pone.0017820. The study reports SRA accession SRA026846.1.
