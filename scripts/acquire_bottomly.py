#!/usr/bin/env python3
"""
Acquire the Bottomly validation dataset for RNA-seq Explorer.

Downloads the raw integer counts and metadata from the ReCount server,
subsets the data to 10 samples (5 C57BL/6J vs 5 DBA/2J) as requested,
formats the columns, and saves them to data/bottomly/.
"""
import argparse
import hashlib
import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

COUNTS_URL = "https://bowtie-bio.sourceforge.net/recount/countTables/bottomly_count_table.txt"
METADATA_URL = "https://bowtie-bio.sourceforge.net/recount/phenotypeTables/bottomly_phenodata.txt"

def compute_sha256(filepath: Path) -> str:
    """Compute the SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def main():
    parser = argparse.ArgumentParser(description="Download the Bottomly validation dataset")
    parser.add_argument("--outdir", default="data/bottomly", help="Output directory")
    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    
    counts_path = outdir / "counts.csv"
    metadata_path = outdir / "metadata.csv"

    logger.info(f"Downloading metadata from {METADATA_URL}")
    # The metadata file is space-separated
    metadata_df = pd.read_csv(METADATA_URL, sep=" ")
    
    # We want 5 C57BL/6J and 5 DBA/2J
    # The original file has 21 samples (10 C57BL/6J, 11 DBA/2J)
    c57 = metadata_df[metadata_df["strain"] == "C57BL/6J"].head(5)
    dba = metadata_df[metadata_df["strain"] == "DBA/2J"].head(5)
    metadata_subset = pd.concat([c57, dba]).copy()
    
    # Clean up column names to match RNA-seq Explorer standard
    metadata_subset = metadata_subset.rename(columns={
        "sample.id": "sample_id",
        "experiment.number": "experiment_number"
    })
    # Keep relevant columns
    metadata_subset = metadata_subset[["sample_id", "strain", "experiment_number"]]
    
    # Standardize condition names to remove special characters that might cause formulaic issues
    metadata_subset["strain"] = metadata_subset["strain"].replace({
        "C57BL/6J": "C57BL_6J",
        "DBA/2J": "DBA_2J"
    })
    
    metadata_subset.to_csv(metadata_path, index=False)
    logger.info(f"Saved metadata to {metadata_path} ({metadata_subset.shape[0]} samples)")

    logger.info(f"Downloading counts from {COUNTS_URL}")
    counts_df = pd.read_csv(COUNTS_URL, sep="\t")
    
    # The index is genes, rename index to gene_id
    counts_df.index.name = "gene_id"
    counts_df = counts_df.reset_index()
    
    # Keep only the 'gene_id' and the selected 10 sample columns
    columns_to_keep = ["gene_id"] + metadata_subset["sample_id"].tolist()
    counts_subset = counts_df[columns_to_keep]
    
    counts_subset.to_csv(counts_path, index=False)
    logger.info(f"Saved counts to {counts_path} ({counts_subset.shape[0]} genes, {counts_subset.shape[1]-1} samples)")
    
    # Compute SHA256 checksums
    counts_hash = compute_sha256(counts_path)
    metadata_hash = compute_sha256(metadata_path)
    
    logger.info(f"counts.csv SHA-256: {counts_hash}")
    logger.info(f"metadata.csv SHA-256: {metadata_hash}")
    
    logger.info("Bottomly dataset successfully acquired.")

if __name__ == "__main__":
    main()
