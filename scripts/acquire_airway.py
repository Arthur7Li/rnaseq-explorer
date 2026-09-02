#!/usr/bin/env python3
"""
Acquire the Airway demo dataset for RNA-seq Explorer.

Downloads the raw integer counts and metadata from the Bioconductor workshops repository,
formats the columns to match RNA-seq Explorer's expected contract, and saves them
to data/airway/.
"""
import argparse
import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

COUNTS_URL = "https://raw.githubusercontent.com/Bioconductor/BiocWorkshops/master/100_Morgan_RBiocForAll/airway_counts.csv"
METADATA_URL = "https://raw.githubusercontent.com/Bioconductor/BiocWorkshops/master/100_Morgan_RBiocForAll/airway_colData.csv"

def main():
    parser = argparse.ArgumentParser(description="Download the Airway demo dataset")
    parser.add_argument("--outdir", default="data/airway", help="Output directory")
    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    
    counts_path = outdir / "counts.csv"
    metadata_path = outdir / "metadata.csv"

    logger.info(f"Downloading counts from {COUNTS_URL}")
    counts_df = pd.read_csv(COUNTS_URL)
    # The first column is named "Gene", we rename it to "gene_id"
    counts_df = counts_df.rename(columns={"Gene": "gene_id"})
    counts_df.to_csv(counts_path, index=False)
    logger.info(f"Saved counts to {counts_path} ({counts_df.shape[0]} genes, {counts_df.shape[1]-1} samples)")

    logger.info(f"Downloading metadata from {METADATA_URL}")
    metadata_df = pd.read_csv(METADATA_URL)
    # The first column is unnamed and holds the sample ID (SRR...)
    metadata_df = metadata_df.rename(columns={
        "Unnamed: 0": "sample_id",
        "cell": "cell_line",
        "dex": "treatment"
    })
    
    metadata_df = metadata_df[["sample_id", "cell_line", "treatment"]]
    
    # Map the levels to match the official config
    metadata_df["treatment"] = metadata_df["treatment"].map({
        "untrt": "untreated",
        "trt": "dexamethasone"
    })
    
    metadata_df.to_csv(metadata_path, index=False)
    logger.info(f"Saved metadata to {metadata_path} ({metadata_df.shape[0]} samples)")
    
    logger.info("Airway dataset successfully acquired.")

if __name__ == "__main__":
    main()
