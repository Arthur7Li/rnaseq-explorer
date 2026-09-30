## Summary

This PR implements **Phase 1: Accessibility & Colorblind-Safe Plots** from the Outstanding Version implementation plan (`docs/OUTSTANDING_PLAN.md`).

## Changes
- **`src/rnax/pipeline/plots.py`**:
  - Adopted the Wong (2011) colorblind-safe palette (`CB_PALETTE` and `WONG_PALETTE`):
    - Up: `"#D55E00"` (vermillion)
    - Down: `"#0072B2"` (blue)
    - Not Significant: `"#999999"` (gray)
  - Added secondary encoding channels (point shapes: triangles `^` for Up, inverted triangles `v` for Down, circles `o` for Not Significant in volcano and MA plots; distinct marker styles in PCA plots).
  - Enforced minimum 12pt axis labels and 14pt titles via `matplotlib.pyplot.rc_context`.
  - Added dynamic, descriptive `alt` text strings returned by all plotting functions.
- **`src/rnax/pipeline/report.py`**:
  - Captured `alt` text return values from plotting functions and passed them to the Jinja2 template context (`plot_alts`).
- **`src/rnax/templates/report.html.j2`**:
  - Added a `<meta name="description">` tag for accessibility.
  - Updated all `<img>` tags to use dynamic, descriptive `alt` text with sensible fallbacks.
- **`tests/test_plots.py` & `tests/test_report.py`**:
  - Added unit test `test_cb_palette_wong` asserting colorblind-safe hex values.
  - Verified that all plot functions return non-empty descriptive `alt` text strings.
  - Added HTML report assertions for `<meta name="description"` and `alt=` attributes.
- **`docs/DECISIONS.md`**:
  - Appended decision **D-8**: Adopt Wong (2011) colorblind-safe palette as standard plot color scheme.

## Test evidence
- `uv run ruff check .` passes with 0 issues.
- `uv run mypy src/` passes with 0 type errors.
- `uv run pytest` passes 40/40 tests.

## Definition of Done
- [x] All acceptance criteria met, no silent scope reduction.
- [x] All existing and new tests pass locally.
- [x] Decision log D-8 recorded.
