# Bottomly Dataset Provenance

## Source Information
- **Name:** Bottomly Validation Dataset (ReCount1)
- **URL:** [ReCount](https://bowtie-bio.sourceforge.net/recount/)
- **Counts URL:** `https://bowtie-bio.sourceforge.net/recount/countTables/bottomly_count_table.txt`
- **Metadata URL:** `https://bowtie-bio.sourceforge.net/recount/phenotypeTables/bottomly_phenodata.txt`
- **Citation:** Bottomly D, Walter NA, Hunter JE, Darakjian P et al. Evaluating gene expression in C57BL/6J and DBA/2J mouse striatum using RNA-Seq and microarrays. PLoS One 2011;6(3):e17820. PMID: 21455293

## Data Policy Compliance
This dataset is a widely used benchmarking standard from the original ReCount project.
- It contains mouse (non-human) data only.
- It contains no clinical, diagnostic, or proprietary information.
- It is freely redistributable for testing and benchmarking purposes.

## Pre-processing and Mapping
The data was downloaded using the `scripts/acquire_bottomly.py` automation script.
1. The metadata and counts were downloaded as raw text files.
2. The dataset was explicitly subsetted to exactly 10 samples (5 C57BL/6J and 5 DBA/2J) to match the Phase 6 implementation plan requirements and speed up CI integration tests.
3. Strain names were sanitized (`C57BL_6J` and `DBA_2J`) to prevent issues with Formulaic model design matrices.
4. The tables were written to `counts.csv` and `metadata.csv` matching RNA-seq Explorer's schema.

## File Integrity Checksums
*Generated automatically by `scripts/acquire_bottomly.py`*

- **`counts.csv` SHA-256**: `6aec596846ad6fe13cecaa3102a23a2e50d0fdb2af5dbf02e2460e0b5e1073fe`
- **`metadata.csv` SHA-256**: `9ccecec16d61a78483d9683dda4bc8da36b34dd21ac41449ec9fa5110e931069`
