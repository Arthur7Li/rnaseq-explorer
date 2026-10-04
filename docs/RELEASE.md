# Release Process

This document outlines the standard operating procedure for cutting a new release of RNA-seq Explorer.

## 1. Prepare the Release

1. **Version Bump:**
   Update the semantic version in the following files:
   - `pyproject.toml` (under `[project] version = "..."`)
   - `src/rnax/__init__.py` (update `__version__`)
   - `CITATION.cff` (update `version:` and `date-released:`)

2. **Update Changelog:**
   Update `CHANGELOG.md` following the [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format. Move anything in `[Unreleased]` into a new version block with the current date.

3. **Commit the Changes:**
   Commit the version bumps to `main` (or via a release PR).
   ```bash
   git add pyproject.toml src/rnax/__init__.py CITATION.cff CHANGELOG.md
   git commit -m "chore: Bump version to v1.X.X"
   git push origin main
   ```

## 2. Tag and Push

Create an annotated git tag and push it to the remote repository.

```bash
git tag -a v1.X.X -m "Release v1.X.X"
git push origin v1.X.X
```

## 3. GitHub Actions Release Automation

Once the tag is pushed, the `.github/workflows/release.yml` action will automatically trigger. This action will:
1. Run the full test suite to ensure stability.
2. Execute the pipeline end-to-end on the `pasilla` dataset.
3. Zip the resulting `results/pasilla/` output directory.
4. Create a draft GitHub Release corresponding to the tag.
5. Attach the `pasilla_example_output.zip` artifact to the release.

## 4. Finalize the Release

1. Navigate to the **Releases** tab in the GitHub repository.
2. Edit the newly created draft release.
3. Copy the relevant section from `CHANGELOG.md` into the release description.
4. Publish the release!
