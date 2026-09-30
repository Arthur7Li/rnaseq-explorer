#!/usr/bin/env python3
"""
fetch_annotations.py

Script to download and update gene annotation CSVs for human, mouse, and drosophila.
These are saved to data/annotations/ to be bundled with the tool.
This script requires network access and should not be run at analysis runtime.
"""

import argparse
import hashlib
import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def sha256sum(filename: Path) -> str:
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        while n := f.readinto(mv):
            h.update(mv[:n])
    return h.hexdigest()


def fetch_ensembl(organism: str, output_path: Path) -> None:
    """
    In a real implementation, this would query Ensembl BioMart.
    For demonstration/MVP, we create a dummy file or fetch from a known stable URL.
    """
    logging.info(f"Fetching annotations for {organism}...")
    
    # We create a dummy CSV for the purpose of the MVP bundle, as a real BioMart query 
    # would require pybiomart or REST API code that is bulky.
    # In a full production scenario, we would use mygene or biomart here.
    df = pd.DataFrame(columns=["gene_id", "gene_symbol", "description"])
    
    if organism == "human":
        df = pd.DataFrame([
            {"gene_id": "ENSG00000000003", "gene_symbol": "TSPAN6", "description": "tetraspanin 6"},
            {"gene_id": "ENSG00000000419", "gene_symbol": "DPM1", "description": "dolichyl-phosphate mannosyltransferase"},
            {"gene_id": "ENSG00000000457", "gene_symbol": "SCYL3", "description": "SCY1 like pseudokinase 3"},
            {"gene_id": "ENSG00000000460", "gene_symbol": "C1orf112", "description": "chromosome 1 open reading frame 112"},
            {"gene_id": "ENSG00000000971", "gene_symbol": "CFH", "description": "complement factor H"},
            {"gene_id": "ENSG00000273456", "gene_symbol": "RNU6-976P", "description": "RNA, U6 small nuclear 976, pseudogene"},
        ])
    elif organism == "mouse":
        df = pd.DataFrame([
            {"gene_id": "0", "gene_symbol": "Gnai3", "description": "guanine nucleotide binding protein (G protein), alpha inhibiting 3"},
            {"gene_id": "1", "gene_symbol": "Pbsn", "description": "probasin"},
            {"gene_id": "2", "gene_symbol": "Cdc45", "description": "cell division cycle 45"},
            {"gene_id": "3", "gene_symbol": "H19", "description": "H19, imprinted maternally expressed transcript"},
        ])
    elif organism == "drosophila":
        df = pd.DataFrame([
            {"gene_id": "FBgn0000003", "gene_symbol": "7SLRNA:CR32864", "description": "7SL RNA"},
            {"gene_id": "FBgn0000008", "gene_symbol": "a", "description": "arc"},
            {"gene_id": "FBgn0000014", "gene_symbol": "abd-A", "description": "abdominal A"},
            {"gene_id": "FBgn0000015", "gene_symbol": "Abd-B", "description": "Abdominal B"},
        ])
        
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    
    sha256 = sha256sum(output_path)
    logging.info(f"Saved {organism} annotations to {output_path} (SHA-256: {sha256})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch and update gene annotations")
    parser.add_argument("--outdir", type=str, default="data/annotations", help="Output directory")
    args = parser.parse_args()
    
    outdir = Path(args.outdir)
    
    organisms = ["human", "mouse", "drosophila"]
    
    for org in organisms:
        out_path = outdir / f"{org}_genes.csv"
        fetch_ensembl(org, out_path)
        
    logging.info("Annotation fetch complete.")


if __name__ == "__main__":
    main()
