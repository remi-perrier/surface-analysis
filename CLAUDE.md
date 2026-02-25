# Surface Analysis - Project Instructions

## Purpose

Python package for analyzing 3D surface topography from microscope measurements.
Decomposes surfaces into form, waviness, roughness, and micro-roughness components
following ISO 25178 / ISO 16610 standards. Built for tube surface characterization.

## Architecture

```
src/surface_analysis/
    __init__.py              # Exports: Surface, Transformation, Transforms
    surface.py               # Surface dataclass + ISO 25178 parameters as properties
    io.py                    # load_datx (Zygo HDF5), generate_synthetic
    viz.py                   # plot_surface, plot_surface_3d, plot_surface_3d_interactive
    transforms/
        _base.py             # Transformation Protocol (runtime_checkable)
        __init__.py          # Transforms catalog (interpolation, projection, filtering)
        interpolation.py     # Linear, Nearest
        projection.py        # Polynomial, Plane
        filtering.py         # Gaussian (ISO 16610-21 sigma)
scripts/
    analyze_yann.py          # Full pipeline on Yann's .datx, saves PNG + HTML to output/
tests/
```

### Key design decisions

- **Surface** is a dataclass holding z (2D height map), step_x, step_y. All units in **mm**.
- **Transformation** is a Protocol with a single method `transform(surface) -> Surface`.
- Concrete transforms inherit the Protocol for readability.
- **Transforms** class aggregates all transforms in 3 categories for discovery.
- Transforms are composable via `surface.apply(*transforms)`.
- Transforms return new surfaces, never mutate input.
- ISO 25178 parameters (Sa, Sq, Sp, Sv, Sz, Ssk, Sku, Sdq, Sdr) are properties on Surface.
- Visualization: `plot()` (2D imshow), `plot_3d()` (matplotlib 3D, subsampled), `plot_3d_interactive()` (plotly HTML). All use lazy imports to keep deps optional.
- All imports are **absolute** (no relative imports).
- `from __future__ import annotations` in every file.
- Transforms validate inputs: no valid points, insufficient points for polynomial degree, non-positive cutoff.

## Usage pattern

```python
from surface_analysis import Surface, Transforms

roughness = (
    Surface.from_datx("measurement.datx")
    .apply(
        Transforms.Interpolation.Linear(),
        Transforms.Projection.Polynomial(degree=2),
        Transforms.Filtering.Gaussian(cutoff=0.8),
    )
)
print(roughness.Sa, roughness.Ssk)
```

## Testing

```bash
uv run python -m pytest tests/ -v
```

- 63 tests across 4 files: `test_surface.py`, `test_io.py`, `test_transforms.py`, `test_viz.py`
- Tests cover: ISO parameters on known surfaces, edge case guards (ValueError), transform immutability, protocol conformance, Transforms catalog, full pipeline composition, visualization (2D, 3D, interactive)

## Tech Stack

- Python 3.12+, managed with **uv**
- numpy, scipy, h5py, matplotlib, plotly
- pytest for testing
- Pre-commit: ruff (lint + format) + mypy, all local via `uv run`

## Git Strategy: Trunk-Based Development

- `main` is always stable
- Feature branches: `feat/<name>`, fixes: `fix/<name>`, research: `research/<name>`
- Short-lived branches, fast-forward merge, delete after merge
- Commit after each coherent unit of work

## Conventions

- Code, comments, commits, docs: English
- Conversation: follow user's language (French/English)
- No over-engineering: build what's needed, iterate
- Surface metrology terminology follows ISO 25178 / ISO 16610
- No relative imports
