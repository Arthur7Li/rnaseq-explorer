# Testing Guide

This directory contains the pytest suite for RNA-seq Explorer.

## Running Tests

Run all unit and integration tests:
```bash
uv run pytest
```

Run only fast tests (skip integration/snapshot tests):
```bash
uv run pytest -m "not slow"
```

## Golden-File Snapshot Testing

We use `pytest-snapshot` to ensure the structure and schemas of our core pipeline outputs (`results.csv`, `report.html`, etc.) do not unintentionally regress.

Snapshot tests are located in `tests/test_snapshots.py` and the golden files are stored inside `tests/snapshots/`.

### Updating Snapshots

If you make an intentional change to the pipeline that alters the expected output (e.g., adding a new column to the results table or a new section to the HTML report), the snapshot tests will fail. 

To bump the golden files to reflect your new intended behavior, run:
```bash
uv run pytest tests/test_snapshots.py --snapshot-update
```
Review the changes to `tests/snapshots/*` via `git diff` and commit them if they accurately reflect your intended changes.

