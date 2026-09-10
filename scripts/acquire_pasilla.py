#!/usr/bin/env python3
"""
Acquire the Pasilla test fixture dataset for RNA-seq Explorer.

Downloads the raw integer counts and metadata from the Bioconductor pasilla package tarball,
formats the columns to match RNA-seq Explorer's expected contract, and saves them
to data/pasilla/.
"""
import argparse
import hashlib
import logging
import tarfile
import urllib.request
from io import BytesIO
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Hardcode the source tarball URL for stability
TARBALL_URL = "https://bioconductor.org/packages/release/data/experiment/src/contrib/pasilla_1.40.0.tar.gz"

def compute_sha256(filepath: Path) -> str:
    """Compute the SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def main():
    parser = argparse.ArgumentParser(description="Download the Pasilla test fixture dataset")
    parser.add_argument("--outdir", default="data/pasilla", help="Output directory")
    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    
    counts_path = outdir / "counts.csv"
    metadata_path = outdir / "metadata.csv"

    logger.info(f"Downloading Bioconductor pasilla bundle from {TARBALL_URL}")
    response = urllib.request.urlopen(TARBALL_URL)
    tarball_bytes = response.read()
    
    logger.info("Extracting counts and metadata from tarball in memory...")
    with tarfile.open(fileobj=BytesIO(tarball_bytes), mode="r:gz") as tar:
        # Extract counts
        counts_member = tar.getmember("pasilla/inst/extdata/pasilla_gene_counts.tsv")
        counts_file = tar.extractfile(counts_member)
        counts_df = pd.read_csv(counts_file, sep="\t")
        
        # Extract metadata
        meta_member = tar.getmember("pasilla/inst/extdata/pasilla_sample_annotation.csv")
        meta_file = tar.extractfile(meta_member)
        metadata_df = pd.read_csv(meta_file)
        
    # Format Counts
    # Gene ID is already named 'gene_id', and samples are like 'untreated1', 'treated1', etc.
    counts_df.to_csv(counts_path, index=False)
    logger.info(f"Saved counts to {counts_path} ({counts_df.shape[0]} genes, {counts_df.shape[1]-1} samples)")

    # Format Metadata
    # The original sample IDs have 'fb' suffix, e.g., 'untreated1fb'
    # We strip 'fb' to match the column names in counts_df
    metadata_df["sample_id"] = metadata_df["file"].str.replace("fb", "", regex=False)
    
    # We only need sample_id and condition for the simple unpaired test
    metadata_df = metadata_df[["sample_id", "condition"]]
    metadata_df.to_csv(metadata_path, index=False)
    logger.info(f"Saved metadata to {metadata_path} ({metadata_df.shape[0]} samples)")
    
    # Compute SHA256 checksums
    counts_hash = compute_sha256(counts_path)
    metadata_hash = compute_sha256(metadata_path)
    
    logger.info(f"counts.csv SHA-256: {counts_hash}")
    logger.info(f"metadata.csv SHA-256: {metadata_hash}")
    
    logger.info("Pasilla dataset successfully acquired.")

if __name__ == "__main__":
    main()
