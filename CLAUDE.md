# Surface Analysis - Project Instructions

## Purpose
Toolkit for analyzing 3D surface topography data from microscope measurements.
Target use case: tube inner/outer surface roughness characterization.

## Architecture

```
src/surface_analysis/   # Library code
  io/                   # Data loading (HDF5/DATAX format)
  preprocessing/        # Interpolation of missing points
  geometry/             # Form removal (cylinder fitting, projection)
  filtering/            # Gaussian/spline filters for component separation
  parameters/           # Roughness parameters (ISO 25178: Sa, Sq, Sz, Ssk, Sku...)
  visualization/        # 2D heatmaps, 3D surface plots
data/
  samples/              # Sample/synthetic data for development
  raw/                  # Real data files (gitignored)
analysis/               # Research notes and analysis documents (markdown)
tests/                  # pytest tests
```

## Tech Stack
- Python 3.12+, managed with `uv`
- numpy, scipy (core computation and filtering)
- h5py (HDF5/DATAX file reading)
- matplotlib (2D heatmaps), plotly (3D interactive)
- No heavy frameworks - keep dependencies minimal and scientific

## Git Strategy: Trunk-Based Development
- `main` branch is always stable
- Feature branches: `feat/<name>`, fixes: `fix/<name>`, research: `research/<name>`
- Short-lived branches, merge via squash
- Commit after each coherent unit of work
- Tags for milestones (v0.1.0 = first working pipeline)

## Conventions
- Code, comments, commits, docs: English
- Conversation: follow user's language (French/English)
- No over-engineering: build what's needed, iterate
- Surface metrology terminology follows ISO 25178 / ISO 16610
- Keep analysis/ notes updated as understanding deepens
