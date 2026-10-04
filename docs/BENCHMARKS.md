# Performance Benchmarks

This document outlines the expected time and computational resources required to run the RNA-seq Explorer differential expression pipeline across various synthetic dataset sizes.

## Local Benchmarks (Apple Silicon)

**Hardware:**
- **Model:** MacBook Air (M2, 2022)
- **CPU:** 8 Cores (4 Performance, 4 Efficiency)
- **RAM:** 8 GB
- **OS:** macOS

**Methodology:**
- Generated synthetic read counts using a negative binomial distribution ($n=10, p=0.1$).
- Configured 8 samples ($N=8$) divided evenly into two biological conditions (4 control vs. 4 treated).
- Measured the real wall-clock time required for specific analytical phases.

| Genes   | Samples | Validation | DESeq2 | Report & Plots | Total  |
|---------|---------|------------|--------|----------------|--------|
| 1,000   | 8       | 0.00s      | 0.98s  | 0.84s          | 1.83s  |
| 5,000   | 8       | 0.01s      | 4.94s  | 1.41s          | 6.36s  |
| 10,000  | 8       | 0.01s      | 9.96s  | 1.75s          | 11.73s |
| 20,000  | 8       | 0.01s      | 19.97s | 2.53s          | 22.52s |
| 50,000  | 8       | 0.03s      | 50.15s | 4.79s          | 54.97s |

*Note: Execution times scale linearly with the number of genes analyzed. Plot generation time (particularly sample distance hierarchical clustering and PCA) also scales with the number of samples.*

## Expected Resource Utilization

- **Small Datasets (e.g., Pasilla, 14k genes, 7 samples):**
  - **Time:** ~10-15 seconds
  - **Memory:** Minimal (< 200MB)
- **Large Datasets (e.g., Human whole genome, 50k+ genes):**
  - **Time:** ~1 minute
  - **Memory:** ~500MB+ peak memory due to heavy array operations during MAP dispersion fitting.
