#!/usr/bin/env python3
import hashlib
import time
from pathlib import Path
from typing import Any

import pandas as pd
import requests

DATA_DIR = Path("data/geo-case-study")
URL = "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE324987&format=file&file=GSE324987%5Fraw%5Fcounts%2Ecsv%2Egz"

def calculate_sha256(filepath: Path) -> str:
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def download_with_retry(url: Any, dest: Any, retries: Any = 5) -> bool:
    for attempt in range(retries):
        try:
            print(f"Downloading (attempt {attempt+1}/{retries})...")
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            with open(dest, "wb") as f:
                f.writelines(response.iter_content(chunk_size=8192))
            return True
        except requests.exceptions.RequestException as e:
            print(f"Failed: {e}")
            time.sleep(2)
    return False

def download_and_extract() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    temp_gz = DATA_DIR / "temp_counts.csv.gz"
    
    if not download_with_retry(URL, temp_gz):
        print("Failed to download after retries.")
        return
        
    print("Reading counts matrix...")
    df = pd.read_csv(temp_gz, index_col=0)
    
    target_samples = [
        "WT-1_S1", "WT-3_S2", "WT-5_S3",
        "1a1bT-3_S7", "1a1bT-4_S8", "1a1bT-5_S9"
    ]
    
    counts_df = df[target_samples].copy()
    counts_df.index.name = "gene_id"
    
    counts_csv = DATA_DIR / "counts.csv"
    counts_df.to_csv(counts_csv)
    print(f"Saved {counts_csv} (Genes: {counts_df.shape[0]}, Samples: {counts_df.shape[1]})")
    
    meta_records = []
    for s in target_samples:
        condition = "wild_type" if s.startswith("WT") else "nrxn1_knockout"
        meta_records.append({
            "sample_id": s,
            "condition": condition
        })
        
    meta_df = pd.DataFrame(meta_records)
    meta_csv = DATA_DIR / "metadata.csv"
    meta_df.to_csv(meta_csv, index=False)
    print(f"Saved {meta_csv}")
    
    temp_gz.unlink()
    
    print("\nFile Checksums (SHA-256):")
    print(f"counts.csv: {calculate_sha256(counts_csv)}")
    print(f"metadata.csv: {calculate_sha256(meta_csv)}")

if __name__ == "__main__":
    download_and_extract()
