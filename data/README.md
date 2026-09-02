# Dataset Directory

This directory contains only small, reviewed derived inputs used for demos and automated tests. It never stores raw sequencing reads, restricted data, or sensitive metadata. See [`docs/DATA_POLICY.md`](../docs/DATA_POLICY.md).

| Folder | Phase | Purpose | Current status | Acquisition path |
|---|---|---|---|---|
| `airway/` | MVP | Human airway smooth-muscle cell treatment demo | Planned; contract, config, script, and provenance record added | Run `Rscript scripts/acquire_airway.R`; complete provenance checklist before committing outputs |
| `bottomly/` | Good Portfolio | Independent mouse-strain validation case | Selected; reviewed source matrix still required | Follow `docs/BOTTOMLY_PLAN.md` data-readiness checklist |
| `pasilla/` | Good Portfolio | Small deterministic CI and tutorial fixture | Selected; reviewed fixture still required | Follow `docs/PASILLA_PLAN.md` review gate |
| `geo-case-study/` | Outstanding | Curated real-world public bulk-RNA-seq case study | Intentionally unselected | Use `docs/GEO_CASE_STUDY_PLAN.md` selection gate |

## Before committing any derived data

1. Validate raw non-negative integer counts and exact count/metadata sample-ID matching.
2. Record source, study/accession, acquisition date, package/database version, annotation, preprocessing history, and reuse terms.
3. Record inclusion/exclusion decisions and SHA-256 checksums in the dataset's `PROVENANCE.md`.
4. Confirm that the dataset has no personal, restricted, or sensitive data.
5. Keep acquisition logic in `scripts/`, not in analysis code or notebooks.
