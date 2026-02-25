# Proposed Implementation Pipeline

## Overview

```
┌──────────┐    ┌───────────────┐    ┌─────────────┐    ┌───────────┐    ┌────────────┐
│  Load    │───▶│ Interpolation │───▶│    Form     │───▶│ Filtering │───▶│ Parameters │
│  Data    │    │ (fill NaN)    │    │  Removal    │    │ (S/L)     │    │ & Viz      │
└──────────┘    └───────────────┘    └─────────────┘    └───────────┘    └────────────┘
   .datx         TPS / griddata      Cylinder fit       Gaussian          Sa, Sq, Sz
   HDF5          bilinear             polynomial         λs, λc            heatmaps
                                      least-squares                        3D plots
```

## Module Breakdown

### 1. `src/surface_analysis/io/` — Data I/O
- `datax_reader.py`: Parse .datx (HDF5) files, extract height map + metadata
- `synthetic.py`: Generate synthetic tube surfaces for testing
- Common output: numpy 2D array (height map) + pixel spacing (dx, dy)

### 2. `src/surface_analysis/preprocessing/` — Interpolation
- `interpolation.py`: Fill non-measured points
  - Detect NaN/invalid mask
  - TPS interpolation (scipy.interpolate.RBFInterpolator)
  - Bilinear fallback for large gaps
  - Report fill statistics (% filled, max gap size)

### 3. `src/surface_analysis/geometry/` — Form Removal
- `leveling.py`: Basic tilt removal (least-squares plane subtraction)
- `cylinder.py`: Cylinder fitting and subtraction
  - Least-squares fit: find center (x₀, z₀), radius R, axis orientation
  - Subtract fitted cylinder to get residual surface
  - Option for polynomial form removal (degree 2-4)

### 4. `src/surface_analysis/filtering/` — Component Separation
- `gaussian.py`: ISO 16610-61 Gaussian filter
  - Input: cutoff wavelength λc + pixel spacing
  - Convert to sigma: σ = λc / (2π × √(2 ln 2)) ≈ λc / 2.9515
  - Apply scipy.ndimage.gaussian_filter with correct sigma in pixels
  - Return: low-pass (waviness) and high-pass (roughness) components
- `pipeline.py`: Full decomposition chain
  - S-filter → L-filter cascade
  - Output: form, waviness, roughness, micro-roughness arrays

### 5. `src/surface_analysis/parameters/` — Roughness Parameters
- `height.py`: Sa, Sq, Sz, Ssk, Sku, Sp, Sv
- `hybrid.py`: Sdq, Sdr
- `spatial.py`: Sal, Str (autocorrelation-based)

### 6. `src/surface_analysis/visualization/` — Plots
- `heatmap.py`: 2D color maps (matplotlib imshow/contourf)
- `surface3d.py`: 3D interactive plots (plotly Surface)
- `profile.py`: Cross-section profiles
- `comparison.py`: Side-by-side before/after views

## Implementation Order

1. **Synthetic data generator** — so we can develop without real data
2. **Basic visualization** — see what we're working with
3. **Form removal** (cylinder fit) — biggest signal to remove first
4. **Gaussian filtering** — core component separation
5. **Roughness parameters** — quantitative output
6. **Interpolation** — needed when real data arrives
7. **DATAX reader** — when we get the actual files

## Synthetic Data Specification

Generate a tube section with known properties:
```python
# Cylinder parameters
R = 5.0          # mm, tube radius
length = 2.0     # mm, measurement length along axis
arc = 30         # degrees, angular span of measurement

# Surface components (superimposed)
form:      cylinder R=5mm
waviness:  sinusoidal, λ=0.5mm, amplitude=2µm
roughness: random Gaussian, σ=0.3µm, correlation length=10µm
noise:     white Gaussian, σ=0.05µm

# Grid
dx = dy = 1µm   # typical for confocal microscope
```

This gives us ground truth to validate each processing step.

## Questions for the Physicist

1. **Instrument**: What microscope model? (Zygo, Keyence, Bruker, Alicona?)
   → Affects .datx reader implementation
2. **Measurement area**: Approximate size in mm? Pixel count?
   → Determines computation performance needs
3. **Tube geometry**: Inner or outer surface? Approximate radius?
   → Affects cylinder fitting approach
4. **Target parameters**: Which roughness parameters does the pro software report?
   → We replicate those first
5. **Cutoff wavelengths**: What λc did the pro software use?
   → We match the same filtering for comparison
6. **Missing data**: Approximately what % of points are non-measured?
   → Determines interpolation strategy
