#!/usr/bin/env Rscript

# Exports the official eight-sample Airway MVP subset.
# Prerequisite: install Bioconductor packages `airway` and `SummarizedExperiment`.

required <- c("airway", "SummarizedExperiment")
missing <- required[!vapply(required, requireNamespace, logical(1), quietly = TRUE)]
if (length(missing) > 0) {
  stop(
    "Missing packages: ", paste(missing, collapse = ", "),
    ". Install with BiocManager::install(c('airway', 'SummarizedExperiment')).",
    call. = FALSE
  )
}

dir.create("data/airway", recursive = TRUE, showWarnings = FALSE)
data("airway", package = "airway", envir = environment())

counts <- SummarizedExperiment::assay(airway)
metadata <- as.data.frame(SummarizedExperiment::colData(airway))
metadata$sample_id <- colnames(counts)

if (!all(c("cell", "dex") %in% names(metadata))) {
  stop("Expected Airway metadata fields `cell` and `dex` were not found.", call. = FALSE)
}
if (ncol(counts) != 8L || length(unique(metadata$cell)) != 4L) {
  stop("Expected eight samples from four cell lines; refusing export.", call. = FALSE)
}
if (!identical(sort(unique(as.character(metadata$dex))), c("trt", "untrt"))) {
  stop("Expected dexamethasone levels `trt` and `untrt`; refusing export.", call. = FALSE)
}
if (any(counts < 0) || any(abs(counts - round(counts)) > 0)) {
  stop("Airway assay is not a non-negative integer count matrix.", call. = FALSE)
}
if (anyDuplicated(rownames(counts)) || anyDuplicated(colnames(counts))) {
  stop("Gene or sample identifiers are not unique; refusing export.", call. = FALSE)
}

counts_export <- data.frame(gene_id = rownames(counts), counts, check.names = FALSE)
metadata_export <- data.frame(
  sample_id = metadata$sample_id,
  cell_line = as.character(metadata$cell),
  treatment = ifelse(as.character(metadata$dex) == "trt", "dexamethasone", "untreated"),
  stringsAsFactors = FALSE
)

write.csv(counts_export, "data/airway/counts.csv", row.names = FALSE, quote = FALSE)
write.csv(metadata_export, "data/airway/metadata.csv", row.names = FALSE, quote = FALSE)
writeLines(capture.output(sessionInfo()), "data/airway/acquisition-sessionInfo.txt")

message("Export complete. Before committing outputs, update data/airway/PROVENANCE.md with package version, acquisition date, source-term review, and SHA-256 checksums.")
