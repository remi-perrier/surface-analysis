# Python Packages Analysis

Research conducted 2026-02-25. All version numbers and release dates verified against PyPI/GitHub.

## Core Stack (already in dependencies)

### numpy / scipy
- **Role**: Foundation for all computation
- **For our use case**:
  - `scipy.ndimage.gaussian_filter`: 2D Gaussian filtering (ISO 16610-61 compliant with proper sigma).
    Implemented as a sequence of 1-D convolutions, supports per-axis sigma, edge handling modes.
  - `scipy.ndimage.median_filter`: Outlier removal, multidimensional median filter.
  - `scipy.ndimage.uniform_filter`: Moving average smoothing (sequence of 1-D uniform filters).
  - `scipy.interpolate.RBFInterpolator`: Thin-plate spline for filling non-measured points.
  - `scipy.optimize.least_squares`: Cylinder fitting for form removal (Levenberg-Marquardt).
  - `scipy.optimize.curve_fit`: Convenience wrapper for non-linear least squares.
  - `scipy.signal`: Butterworth, Chebyshev filters; `detrend` for polynomial removal.
  - `numpy.linalg.lstsq`: Polynomial surface fitting for leveling/form removal.
  - `numpy.fft.fft2` / `numpy.fft.rfft2`: Power spectral density computation.
- **Version**: scipy 1.15.x, numpy 2.4.x (latest stable as of 2026-02)
- **Verdict**: Essential. Already installed.

### h5py
- **Role**: Read HDF5 / DATAX files
- **Latest version**: 3.15.1 (released 2025-10-16)
- **Python support**: >= 3.10, wheels for CPython 3.12 and 3.13
- **License**: BSD-3-Clause
- **For our use case**: Direct access to .datx files from Zygo instruments.
  HDF5 files are containers of datasets (array-like) and groups (dict-like).
  h5py exposes them as numpy arrays with pythonic dict-style access.
- **Note**: Not yet compatible with Python free-threading mode.
- **Verdict**: Essential. Already installed.

### matplotlib
- **Role**: 2D visualization (heatmaps, profiles, histograms)
- **For our use case**: `imshow` for height maps, `contourf` for contours, profile plots
- **Verdict**: Essential for publication-quality 2D plots. Already installed.

### plotly
- **Role**: Interactive 3D visualization
- **For our use case**: `plotly.graph_objects.Surface` for interactive 3D surface plots.
  Supports colorscale mapping, contour lines on surface (`contours_z`), lighting control.
  Also `px.imshow()` for quick 2D heatmaps with hover data.
- **Verdict**: Good for exploration. Already installed.

---

## Specialized Surface Metrology Packages

### surfalize
- **Repository**: https://github.com/fredericjs/surfalize
- **Documentation**: https://surfalize.readthedocs.io/en/stable/
- **Latest version**: 0.16.7 (released 2026-01-02)
- **Recent activity**: 732 commits, regular releases throughout 2025
  (0.16.0 through 0.16.7 between March 2025 and Jan 2026)
- **Published**: Schell et al., MDPI Nanomaterials 14(13), 1076 (2024)
- **License**: GPL-3.0
- **Language**: Pure Python (no C compiler needed), 62 stars, 19 forks

**Supported file formats** (15+ formats):

| Manufacturer    | Extension        | Read | Write |
|-----------------|------------------|------|-------|
| Keyence         | .vk4, .vk6, .vk7| Yes  | No    |
| Keyence         | .cag             | Extraction | No |
| Leica           | .plu             | Yes  | No    |
| Sensofar        | .plu, .plux      | Yes  | No    |
| Digital Surf    | .sur             | Yes  | Yes   |
| KLA Zeta        | .zmg             | Yes  | No    |
| Wyko            | .opd             | Yes  | No    |
| Nanofocus       | .nms             | Yes  | No    |
| Alicona         | .al3d            | Yes  | Yes   |
| Digital Surf    | .sdf             | Yes  | Yes   |
| Gwyddion        | .gwy             | Yes  | No    |
| Digital Metrology| .os3d           | Yes  | No    |
| IAU FITS        | .fits            | Yes  | No    |
| Zygo            | .dat             | Yes  | No    |
| OpenFMC         | .x3p             | Yes  | No    |
| TrueMap         | .tmd             | Yes  | Yes   |
| General         | .xyz             | Yes  | No    |

**Note**: Supports `.dat` (Zygo MetroPro binary) but NOT `.datx` (Zygo HDF5). For `.datx` we need our own reader or SurfaceTopography.

**ISO 25178 parameters implemented** (20+ parameters):
- Height: Sa, Sq, Sp, Sv, Sz, Ssk, Sku
- Hybrid: Sdr, Sdq
- Spatial: Sal, Str
- Functional (bearing curve): Sk, Spk, Svk, Smr1, Smr2, Sxp
- Functional volume: Vmp, Vmc, Vvv, Vvc
- Profile roughness: "undocumented and not conforming to ISO standards" (per their docs)

**Processing operations**:
- Leveling: least-squares plane subtraction via `.level()`
- Gaussian filtering: highpass, lowpass, bandpass via `.filter('highpass', cutoff=10)`
  - GaussianFilter class with proper ISO cutoff (50% amplitude at cutoff wavelength)
- Outlier removal: `.remove_outliers()` using median filter
- Fill non-measured: `.fill_nonmeasured(method='nearest')`
- Rotation, alignment, cropping, thresholding
- All operations support `inplace=True` and method chaining

**Visualization**:
- `.show()` for topography display (colormap, mask colors)
- `.plot_abbott_curve()` for Abbott-Firestone / bearing area curve
- `.plot_fourier_transform()` for frequency analysis

**Batch processing**: Built-in batch API for processing multiple files.

**Pros**: Pure Python, actively maintained, peer-reviewed, ISO-compliant parameters,
good filtering with proper Gaussian cutoff semantics.
**Cons**: Does NOT read `.datx` Zygo HDF5 format (only `.dat`). Focused on periodic
surface structures (LIPSS, DLIP). No cylinder form removal built-in.
**Verdict**: Strong candidate for parameter validation. Add as optional dependency.

### SurfaceTopography (ContactEngineering)
- **Repository**: https://github.com/ContactEngineering/SurfaceTopography
- **Cloud platform**: https://contact.engineering
- **Latest version**: 1.20.0 (released 2026-01-10)
- **Recent activity**: Very active -- 7 releases in 2025, latest in Jan 2026
  (1.18.0 to 1.20.0 between March 2025 and January 2026)
- **Python support**: 3.8 - 3.12 (wheels available)
- **License**: MIT
- **History**: Refactored from PyCo into three modules: SurfaceTopography, ContactMechanics, Adhesion

**Supported file formats** (35+ formats, the broadest coverage):
- Alicona AL3D, Bruker DI, Nanosurf EZD, Igor Pro IBW, JPK
- Olympus LEXT/OIR/POIR, Wyko OPD/OPDX
- **Zygo DATX and MetroPro** (confirmed .datx support)
- Keyence PS/VK/ZON
- BCR-STM, Nanofocus NMS, PTB NMM
- Generic: ASCII, HDF5, NetCDF, NumPy, MATLAB, XYZ
- Standards: X3P (ISO 25178-72), SDF (ISO 25178-71)
- NASA SRTM HGT, Gwyddion GWY

**Analysis capabilities**:
- RMS height, power spectral density (PSD), autocorrelation function (ACF)
- Variable bandwidth analysis
- Non-uniform topography support (scattered data, not just grids)
- Auto-format detection via `read_topography()`

**Pros**: Reads `.datx` natively. 35+ formats. Mature, scientific, backed by
contact.engineering cloud platform. MIT license (more permissive than surfalize's GPL-3.0).
**Cons**: Heavier dependency chain (needs Cython compilation, meson build system).
More oriented toward contact mechanics and multi-scale analysis than ISO 25178 parameters.
Does not directly expose Sa/Sq/Sz the way surfalize does.
**Verdict**: Best option for reading .datx files. Could use it just for I/O.

### SurfILE
- **Repository**: https://github.com/andeledea/surfile
- **Paper**: MDPI Metrology 4(4), 41 (2024)
- **What it does**: Form operators, slope distributions, PSD, stitching routines, profile extraction
- **Unique feature**: Stitching algorithms (cross-correlation + point cloud registration)
  for samples wider than instrument field of view
- **Status**: Newer, less established, fewer users
- **Verdict**: Keep as reference. Stitching capability could be useful later.

### prysm
- **Repository**: https://github.com/brandondube/prysm
- **Latest version**: 0.21.1
- **What it does**: Physical optics module. Includes Zygo .datx reader (requires h5py).
  Used by interferometer vendors to cross-validate their software.
- **Relevance**: Has a dedicated I/O module for Zygo files, but the package is focused
  on optical system modeling, not surface metrology.
- **Verdict**: Reference for .datx reading implementation if SurfaceTopography is too heavy.

---

## Visualization Alternatives

### pyvista
- **Latest version**: 0.46.3 (released 2025-08-26), docs at 0.47.1
- **Python support**: >= 3.10
- **License**: MIT
- **What it does**: 3D mesh visualization wrapping VTK. Used by 2000+ open-source projects.
  Active community (SciPy 2024 and 2025 tutorials).
- **For our use case**: `pyvista.StructuredGrid` for surface height maps, interactive 3D rendering,
  good for large datasets, Jupyter integration (server + client-side rendering).
- **Pros**: Powerful for 3D rendering, interactive, handles large meshes well
- **Cons**: Heavy dependency (VTK ~200MB), overkill for surface maps
- **Verdict**: Not needed initially. plotly + matplotlib sufficient.
  Consider if rendering performance becomes an issue with large datasets.

---

## DATAX (.datx) File Format Details

The `.datx` format is Zygo's modern HDF5-based file format, used by their Mx software.
It replaced the older binary `.dat` (MetroPro) format.

**HDF5 structure** (based on community gist and SurfaceTopography source):
```
Root
└── Data
    └── Surface
        └── [measurement name]
            ├── vals          (Dataset: 2D float array, the height map)
            └── attrs
                ├── "No Data"     (sentinel value for non-measured points)
                └── "Z Converter"
                    └── "BaseUnit"  (measurement unit: nm, um, mm, etc.)
```

**Key characteristics**:
- Height map stored as 2D numpy-compatible float array
- Non-measured points marked with a sentinel value ("No Data" attribute), convert to `np.nan`
- Units stored as attributes on the Z converter
- Lateral resolution (pixel spacing) stored in metadata attributes
- Additional layers possible: intensity, phase, RGB images

**Reading approaches** (in order of preference):
1. `SurfaceTopography.read_topography('file.datx')` -- auto-detects format, returns rich object
2. Custom h5py reader -- minimal dependencies, full control (reference gist: https://gist.github.com/g-s-k/ccffb1e84df065a690e554f4b40cfd3a)
3. `prysm.io` module -- also reads .datx, but pulls in all of prysm

**Zygo's stance**: "ZYGO file formats are documented, supported and open."

---

## Sample Data Strategy

### Option 1: Synthetic generation (recommended to start)
- Generate a cylinder surface + waviness + roughness + noise with known ground truth
- Use `numpy.random` for Gaussian roughness, sinusoids for waviness
- We control all parameters, enabling validation of each pipeline step

### Option 2: contact.engineering platform
- Public datasets at https://contact.engineering
- FAIR database with DOIs, published by researchers worldwide
- Real measurement data from various instruments
- Can download and use with `SurfaceTopography.read_topography()`

### Option 3: The Surface-Topography Challenge
- Published 2025 on Zenodo: https://zenodo.org/records/15341939
- Multi-laboratory benchmark study (70+ institutions)
- ~36.6 GB of wafer topography measurements
- CC0/CC-BY-4.0 licensed

### Option 4: Synthetic rough surface generators
- **Pyrough**: Builds virtual samples with configurable roughness using self-affine / fractal surfaces.
  Sum of cosine functions with power-law amplitudes. Open source. (https://github.com/Music-Cognition-Lab/pyrough)
- **rough-surface-generation**: FFT-based method using inverse Fourier transform with user-defined PSD.
  (https://github.com/hemingqin/rough-surface-generation)
- **SurfaceTopography** itself can generate synthetic surfaces with prescribed PSD

### Recommendation
Start with our own synthetic data generator (simple, no extra dependencies, known ground truth).
Use contact.engineering datasets for validation against real-world measurements later.

---

## Decision: Start Minimal

**Phase 1 dependencies** (what we have):
- numpy, scipy, h5py, matplotlib, plotly

**Phase 2** (add when needed):
- `surfalize`: For validated ISO 25178 parameter computation and cross-checking our implementations
- `SurfaceTopography`: If we need to read .datx files before building our own reader,
  or for accessing the contact.engineering ecosystem

**Phase 3** (if needed):
- `pyvista`: If plotly 3D performance is insufficient for large datasets

**Build ourselves** (with scipy/numpy):
- DATAX reader (h5py wrapper targeting Zygo .datx HDF5 structure)
- Cylinder fitting / form removal (scipy.optimize.least_squares)
- Missing point interpolation (scipy.interpolate.RBFInterpolator)
- Gaussian filter wrapper with ISO cutoff conventions (scipy.ndimage.gaussian_filter)
- Basic roughness parameters (Sa, Sq, Sz, Ssk, Sku) -- straightforward formulas on arrays
- Hybrid parameters (Sdq, Sdr) -- gradient-based, also straightforward

This keeps the dependency tree minimal and gives us full control.
We can validate our implementations against surfalize later.

---

## Quick Reference: Package Comparison

| Feature                       | surfalize      | SurfaceTopography | scipy/numpy    |
|-------------------------------|----------------|-------------------|----------------|
| Read .datx (Zygo HDF5)       | No (.dat only) | Yes               | Via h5py       |
| ISO 25178 parameters          | 20+ params     | PSD/ACF/RMS       | Build manually |
| Gaussian filtering (ISO)      | Yes            | Limited            | Build wrapper  |
| Cylinder form removal         | No             | No                 | Build manually |
| File format coverage          | 15+ formats    | 35+ formats        | N/A            |
| License                       | GPL-3.0        | MIT                | BSD            |
| Dependencies                  | Light (pure Py)| Medium (Cython)    | Already there  |
| PyPI latest release           | 2026-01-02     | 2026-01-10         | N/A            |

Sources:
- https://github.com/fredericjs/surfalize
- https://github.com/ContactEngineering/SurfaceTopography
- https://surfalize.readthedocs.io/en/stable/
- https://pypi.org/project/surfalize/
- https://pypi.org/project/SurfaceTopography/
- https://pypi.org/project/h5py/
- https://github.com/pyvista/pyvista
- https://gist.github.com/g-s-k/ccffb1e84df065a690e554f4b40cfd3a
- https://zenodo.org/records/15341939
- https://contact.engineering
- https://pmc.ncbi.nlm.nih.gov/articles/PMC11243480/
