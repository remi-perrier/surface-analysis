# Python Packages Analysis

## Core Stack (already in dependencies)

### numpy / scipy
- **Role**: Foundation for all computation
- **For our use case**:
  - `scipy.ndimage.gaussian_filter`: 2D Gaussian filtering (ISO 16610-61 compliant with proper sigma)
  - `scipy.interpolate`: thin-plate spline, RBF interpolation, griddata for missing points
  - `scipy.optimize.least_squares`: cylinder fitting for form removal
  - `scipy.signal`: additional filtering tools (butterworth, etc.)
  - `numpy.linalg.lstsq`: polynomial surface fitting for leveling
- **Verdict**: Essential. Already installed.

### h5py
- **Role**: Read HDF5 / DATAX files
- **For our use case**: Direct access to .datx files from Zygo instruments
- **Verdict**: Essential. Already installed.

### matplotlib
- **Role**: 2D visualization (heatmaps, profiles, histograms)
- **For our use case**: `imshow` for height maps, `contourf` for contours, profile plots
- **Verdict**: Essential for publication-quality 2D plots. Already installed.

### plotly
- **Role**: Interactive 3D visualization
- **For our use case**: `plotly.graph_objects.Surface` for interactive 3D surface plots
- **Verdict**: Good for exploration. Already installed.

## Specialized Packages to Evaluate

### surfalize
- **Repository**: https://github.com/fredericjs/surfalize
- **Published**: MDPI Nanomaterials (2024)
- **What it does**:
  - ISO 25178 parameters (Sa, Sq, Sz, Ssk, Sku, Sdq, Sdr, Sal, Str...)
  - Gaussian filtering
  - Leveling and form removal
  - File format readers (many instruments supported)
- **Pros**: Pure Python, actively maintained, peer-reviewed, ISO-compliant
- **Cons**: Focused on periodic surface structures (LIPSS, DLIP), may not handle cylinder form
- **Verdict**: Strong candidate. Could save us implementing ISO parameters from scratch.

### SurfaceTopography (ContactEngineering)
- **Repository**: https://github.com/ContactEngineering/SurfaceTopography
- **What it does**:
  - Read many surface formats
  - PSD, autocorrelation, roughness parameters
  - Non-uniform topography support
  - Part of contact.engineering platform
- **Pros**: Mature, scientific, extensive format support
- **Cons**: More oriented toward contact mechanics, heavier dependency chain
- **Verdict**: Worth evaluating if surfalize doesn't cover our needs.

### SurfILE
- **Repository**: https://www.mdpi.com/2673-8244/4/4/41
- **What it does**: Open-source surface topography analysis
- **Status**: Newer, less established
- **Verdict**: Keep as reference, prefer surfalize.

## Visualization Alternatives

### pyvista
- **What it does**: 3D mesh visualization wrapping VTK
- **Pros**: Powerful for 3D rendering, interactive, good for large datasets
- **Cons**: Heavy dependency (VTK), overkill for surface maps
- **Verdict**: Not needed initially. plotly + matplotlib sufficient for our use case.

## Decision: Start Minimal

**Phase 1 dependencies** (what we have):
- numpy, scipy, h5py, matplotlib, plotly

**Phase 2** (add if needed):
- surfalize: if we want validated ISO 25178 parameter computation
- pyvista: if plotly 3D performance is insufficient

**Build ourselves**:
- DATAX reader (h5py wrapper, specific to Zygo structure)
- Cylinder fitting / form removal (scipy.optimize)
- Missing point interpolation (scipy.interpolate)
- Gaussian filter wrapper with ISO cutoff conventions (scipy.ndimage)
- Basic roughness parameters (Sa, Sq, Sz, Ssk, Sku) — straightforward formulas

This keeps the dependency tree minimal and gives us full control.
We can validate our implementations against surfalize later.

## Sample Data Strategy

**Option 1: Synthetic generation** (recommended to start)
- Generate a cylinder surface + waviness + roughness + noise
- Known ground truth for validating our pipeline
- We control all parameters

**Option 2: contact.engineering platform**
- Public datasets available at https://contact.engineering
- Real measurement data, but may not be tube geometry

**Option 3: Wait for real data**
- User will provide .datx files
- We build the reader, everything else works on numpy arrays

**Recommendation**: Start with synthetic data to build and validate the pipeline,
then adapt the I/O layer when real data arrives.
