# Surface Metrology Analysis - Subject Understanding

## Context

A physicist uses a microscope (likely confocal or interferometric) to measure the 3D topography
of a tube's surface. The instrument produces a point cloud (x, y, z) representing surface height
at each measured position. The goal is to characterize **surface roughness** by isolating it from
other surface components.

## The 4 Surface Components

A measured surface is decomposed into components by spatial wavelength:

```
Measured surface = Form + Waviness + Roughness + Micro-roughness
                   ↑         ↑          ↑            ↑
              Largest λ                          Smallest λ
```

| Component       | Description                           | Typical wavelengths  |
|-----------------|---------------------------------------|----------------------|
| **Form**        | Macro geometry (cylinder, sphere...)  | > λf (longest)       |
| **Waviness**    | Medium-scale undulations              | λc to λf             |
| **Roughness**   | Process marks, grain structure        | λs to λc             |
| **Micro-roughness** | Instrument noise, sub-micron features | < λs (shortest) |

### Standard Cutoff Wavelengths (ISO 4288 / ISO 25178-3)

- **λs** (S-filter): separates micro-roughness from roughness. Typical: 2.5 µm, 8 µm
- **λc** (L-filter): separates roughness from waviness. Typical: 0.08, 0.25, 0.8, 2.5 mm
- **λf** (F-operator): separates waviness from form. Application-dependent
- Standard bandwidth ratio: λc/λs = 300 (ISO convention)

## The 3 Processing Steps

### 1. Interpolation (Missing Points)

Optical microscopes can produce non-measured points (NaN/invalid) due to:
- Steep slopes exceeding instrument capability
- Low reflectivity areas
- Shadowing effects

**Methods:**
- Nearest-neighbor interpolation (fast, rough)
- Bilinear/bicubic interpolation (smooth)
- Thin-plate spline (TPS): minimizes bending energy, physically motivated, smooth result
- Inpainting algorithms (from image processing)

Thin-plate spline is the preferred method in professional software (Digital Surf MountainsMap).

### 2. Form Removal (Projection for Tube Geometry)

Since the measured surface is a section of a cylinder, the dominant signal is the cylindrical form.
This must be removed before roughness analysis.

**F-operator approaches:**
- **Least-squares cylinder fitting**: fit a cylinder (x-x₀)² + (z-z₀)² = R² to the data,
  subtract it. This is the standard approach for tube surfaces.
- **Polynomial fitting**: fit and subtract a polynomial surface (degree 2+ for curvature).
  Warning: high-degree polynomials diverge at edges.
- **Minimum zone method**: L∞-norm fitting (Chebyshev), encloses surface between parallel shapes.

For a tube, least-squares cylinder fitting is the correct physical approach.

### 3. Filtering (Component Separation)

After form removal, filters separate waviness from roughness from micro-roughness.

**Filter types (ISO 16610):**

| Filter | Standard | Description |
|--------|----------|-------------|
| **Gaussian** | ISO 16610-21 (profile), -61 (areal) | Standard low-pass, 50% transmission at cutoff. Robust variant available. |
| **Spline** | ISO 16610-22 (profile), -62 (areal) | Cubic spline with tension β. β=0.6252 ≈ Gaussian behavior. |
| **Morphological** | ISO 16610-41 (profile), -81 (areal) | Opening/closing with structuring element. For functional surfaces. |

**Gaussian filter** is the default choice. It acts as a weighted moving average with a Gaussian kernel.
At the cutoff wavelength, 50% of the amplitude is transmitted.

**Filter chain for full decomposition:**
```
Measured → [F-operator] → Primary surface (form removed)
                ↓
         [S-filter (λs)] → SF surface (micro-roughness removed)
                ↓
         [L-filter (λc)] → Roughness (short λ) + Waviness (long λ)
```

## Key Surface Parameters (ISO 25178-2)

### Height Parameters
| Parameter | Name | Description |
|-----------|------|-------------|
| **Sa** | Arithmetic mean height | 3D extension of Ra. Mean absolute deviation. |
| **Sq** | Root mean square height | 3D extension of Rq. RMS deviation. |
| **Sz** | Maximum height | Highest peak to deepest valley. |
| **Ssk** | Skewness | Asymmetry of height distribution. <0 = valleys dominate. |
| **Sku** | Kurtosis | Sharpness of distribution. =3 for Gaussian surface. |
| **Sp** | Maximum peak height | Highest point above mean plane. |
| **Sv** | Maximum valley depth | Deepest point below mean plane. |

### Hybrid Parameters
| Parameter | Name | Description |
|-----------|------|-------------|
| **Sdq** | RMS gradient | Local slope complexity. Higher = more complex. |
| **Sdr** | Developed area ratio | % excess of real area over projected area. |

### Spatial Parameters
| Parameter | Name | Description |
|-----------|------|-------------|
| **Sal** | Autocorrelation length | Fastest decay of autocorrelation. |
| **Str** | Texture aspect ratio | 0=anisotropic, 1=isotropic. |

## Relevant Standards

- **ISO 25178**: Areal surface texture (parameters, measurement, instruments)
- **ISO 16610**: Filtration methods (Gaussian, spline, morphological, wavelets)
- **ISO 4287/21920**: Profile roughness parameters (Ra, Rq, Rz...)
- **ISO 4288/21920-3**: Rules for cutoff selection

## Data Format: DATAX (.datx)

The `.datx` format is an **HDF5-based format from Zygo** (used with MetroPro/Mx software).
It stores surface topography data with metadata (measurement parameters, instrument info).

- Can be read with `h5py` in Python
- Structure: hierarchical groups containing datasets (height map, intensity, phase...)
- A community gist exists for parsing: https://gist.github.com/g-s-k/ccffb1e84df065a690e554f4b40cfd3a

Other instrument makers (Bruker, Keyence, Alicona) have their own formats, but if the user
confirms HDF5/DATAX, we target Zygo format first.
