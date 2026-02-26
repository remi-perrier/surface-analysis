# ISO Standards Reference for Surface Metrology

Reference document for the surface_analysis package.
Covers the ISO norms relevant to surface topography decomposition, filtering, and parameter calculation.

---

## Overview

Three standard families govern surface texture analysis:

| Family | Scope |
|---|---|
| **ISO 25178** | Areal (3D) surface texture — parameters, terms, instruments |
| **ISO 16610** | Filtration — Gaussian, spline, morphological, robust, wavelet |
| **ISO 4287/4288** | Profile (2D) parameters and measurement rules (legacy, being superseded by ISO 21920) |

---

## ISO 25178 — Areal Surface Texture

Defines 3D surface texture analysis. Parameters use prefix **S** (or **V** for volume).

### Parts relevant to this project

| Part | Title | Relevance |
|---|---|---|
| **25178-1** | Indication of surface texture | Symbology on drawings |
| **25178-2** | Terms, definitions and parameters | **All S-parameters defined here** |
| **25178-3** | Specification operators | How to specify filtering + evaluation |
| **25178-6** | Classification of methods | Contact vs optical instruments |
| **25178-601 to 607** | Nominal characteristics of instruments | Interferometry, confocal, focus variation... |

### ISO 25178-2 — Areal Parameters

#### Height parameters (implemented)

| Symbol | Name | Definition |
|---|---|---|
| **Sa** | Arithmetic mean height | Mean absolute deviation from the mean plane |
| **Sq** | Root mean square height | RMS of height distribution |
| **Ssk** | Skewness | Asymmetry of the height distribution (0 = symmetric) |
| **Sku** | Kurtosis | Sharpness of the height distribution (3 = Gaussian) |
| **Sp** | Maximum peak height | Highest point above mean plane |
| **Sv** | Maximum valley depth | Deepest point below mean plane |
| **Sz** | Maximum height | Sp + Sv |

#### Hybrid parameters (implemented)

| Symbol | Name | Definition |
|---|---|---|
| **Sdq** | Root mean square gradient | RMS of local surface slopes |
| **Sdr** | Developed interfacial area ratio | % excess of real area vs projected area |

#### Spatial parameters (not yet implemented)

| Symbol | Name | Definition |
|---|---|---|
| **Sal** | Autocorrelation length | Fastest decay length of the autocorrelation function |
| **Str** | Texture aspect ratio | Isotropy indicator: 0 = anisotropic, 1 = isotropic |
| **Std** | Texture direction | Dominant orientation angle (degrees) |

#### Functional parameters — Abbott-Firestone curve (not yet implemented)

Derived from the areal material ratio curve (Abbott-Firestone curve).

| Symbol | Name | Definition |
|---|---|---|
| **Sk** | Core roughness depth | Height of the core surface (linear region) |
| **Spk** | Reduced peak height | Mean height of peaks above the core |
| **Svk** | Reduced valley depth | Mean depth of valleys below the core |
| **Smr1** | Upper material ratio | Material ratio at the top of the core (%) |
| **Smr2** | Lower material ratio | Material ratio at the bottom of the core (%) |

#### Volume parameters (not yet implemented)

| Symbol | Name | Definition |
|---|---|---|
| **Vmp** | Peak material volume | Material volume of the peak zone |
| **Vmc** | Core material volume | Material volume of the core zone |
| **Vvc** | Core void volume | Void volume of the core zone |
| **Vvv** | Valley void volume | Void volume of the valley zone |

*Units: ml/m² or µm³/mm²*

---

## ISO 16610 — Filtration

Defines all filter types used to separate surface components at different scales.

### Parts relevant to this project

| Part | Scope | Filter type | Status in package |
|---|---|---|---|
| **16610-21** | Profile: Gaussian filter | Linear, isotropic | **Implemented** |
| **16610-22** | Profile: Spline filter | Linear, cubic spline | Not implemented |
| **16610-29** | Profile: Wavelet filter | Spline wavelets | Not implemented |
| **16610-31** | Profile: Robust Gaussian regression | Handles outliers/steps | Not implemented |
| **16610-32** | Profile: Robust spline filter | Robust, non-linear | Not implemented |
| **16610-41** | Profile: Morphological filter | Dilation/erosion envelopes | Not implemented |
| **16610-61** | **Areal: Gaussian filter** | Extension of -21 to surfaces | **Implemented** |
| **16610-62** | Areal: Spline filter | Extension of -22 to surfaces | Not implemented |
| **16610-69** | Areal: Wavelet filter | Extension of -29 to surfaces | Not implemented |
| **16610-81** | Areal: Morphological filter | Extension of -41 to surfaces | Not implemented |

### ISO 16610-21 / 16610-61 — Gaussian Filter (implemented)

The reference filter for surface metrology.

**Key properties:**
- Transmission at cutoff wavelength = **50%** of amplitude
- Sigma conversion: `σ = λc × √(ln2 / (2π²))` per ISO 16610-21
- Separates surface into short-wave (highpass) and long-wave (lowpass) components
- `highpass + lowpass = original` (perfect reconstruction)
- Standard cutoff ratio: **λc / λs = 300:1**

### When to use other filters

| Filter | Use case |
|---|---|
| **Robust Gaussian** (16610-31) | Surfaces with outliers, scratches, steps, or deep defects |
| **Morphological** (16610-41/81) | Envelope-based analysis; separating particles from substrate |
| **Spline** (16610-22/62) | Similar to Gaussian but better end-effect handling |
| **Wavelet** (16610-29/69) | Localized scale analysis; identifying features at specific locations |

---

## ISO 4288 — Cutoff Selection Rules

Defines how to select the cutoff wavelength λc based on measured roughness.
Originally for profiles (2D), but the cutoff values apply to areal (3D) analysis too.

### Standard cutoff values

The five standard λc values form a geometric progression (factor ≈ 3):

```
0.08 — 0.25 — 0.8 — 2.5 — 8 mm
```

### Selection tables

#### Non-periodic profiles — by Ra

| Ra (µm) | λc (mm) | Evaluation length (mm) |
|---|---|---|
| Ra ≤ 0.02 | 0.08 | 0.4 |
| 0.02 < Ra ≤ 0.1 | 0.25 | 1.25 |
| 0.1 < Ra ≤ 2 | **0.8** | 4 |
| 2 < Ra ≤ 10 | 2.5 | 12.5 |
| 10 < Ra ≤ 80 | 8 | 40 |

#### Non-periodic profiles — by Rz

| Rz (µm) | λc (mm) | Evaluation length (mm) |
|---|---|---|
| Rz ≤ 0.1 | 0.08 | 0.4 |
| 0.1 < Rz ≤ 0.5 | 0.25 | 1.25 |
| 0.5 < Rz ≤ 10 | **0.8** | 4 |
| 10 < Rz ≤ 50 | 2.5 | 12.5 |
| 50 < Rz ≤ 200 | 8 | 40 |

#### Periodic profiles — by RSm

| RSm (mm) | λc (mm) | Evaluation length (mm) |
|---|---|---|
| 0.013 < RSm ≤ 0.04 | 0.08 | 0.4 |
| 0.04 < RSm ≤ 0.13 | 0.25 | 1.25 |
| 0.13 < RSm ≤ 0.4 | **0.8** | 4 |
| 0.4 < RSm ≤ 1.3 | 2.5 | 12.5 |
| 1.3 < RSm ≤ 4 | 8 | 40 |

### Short-wavelength cutoff λs

The standard recommends a bandwidth ratio of **λc / λs = 300:1**:

| λc (mm) | λs (µm) |
|---|---|
| 0.08 | 0.27 |
| 0.25 | 0.83 |
| 0.8 | 2.5 |
| 2.5 | 8.3 |
| 8 | 25 |

*λs is converted to mm for use in the package: e.g. λs = 2.5 µm = 0.0025 mm.*

---

## Surface Decomposition Model

The ISO standard decomposition of a measured surface:

```
Measured surface
  │
  ├─ Form removal (fit nominal geometry: plane, cylinder, sphere, polynomial)
  │   Method: least-squares fit per ISO 25178-2
  │
  └─ Primary surface (form removed)
      │
      ├─ Lowpass(λc) → Waviness         λ > λc
      │
      └─ Highpass(λc)
          │
          ├─ Lowpass(λs) → Roughness     λs < λ < λc   (bandpass)
          │
          └─ Highpass(λs) → Micro-roughness / noise    λ < λs
```

**Key relationships:**
- `waviness + roughness + micro_roughness ≈ primary surface`
- `roughness = highpass(λc) - highpass(λs)` = bandpass
- Form removal is **not** filtering — it's geometric fitting (least-squares)
- The filter is always **Gaussian** (ISO 16610-21/61) unless otherwise specified

---

## Sources

- [Digital Surf — Surface Metrology Guide](https://guide.digitalsurf.com/en/guide.html)
- [Digital Surf — Areal Field Parameters](https://guide.digitalsurf.com/en/guide-areal-field-parameters.html)
- [Digital Surf — Areal Functional Parameters](https://guide.digitalsurf.com/en/guide-areal-functional-parameters.html)
- [Digital Surf — Filtration Techniques](https://guide.digitalsurf.com/en/guide-filtration-techniques.html)
- [Digital Surf — International Standards](https://guide.digitalsurf.com/en/guide-metrology-standards.html)
- [Keyence — Measurement Procedure (ISO 4288 tables)](https://www.keyence.com/ss/products/microscope/roughness/line/measurement_procedure.jsp)
- [Mahr — Selecting the Correct Filter](https://www.mahr.com/en-us/news-events/article-view/surface-measurement-selecting-the-correct-filter)
- [ISO 16610-21:2011 (official)](https://www.iso.org/standard/50176.html)
- [ISO 25178-2:2021 (official)](https://www.iso.org/standard/74591.html)
- [PTB — Selected Filtration Methods of ISO 16610 (PDF)](https://www.ptb.de/cms/fileadmin/internet/fachabteilungen/abteilung_5/5.1_oberflaechenmesstechnik/DKD-Richtlinien/Selected_Filtration_Methods_of_ISO-16610.pdf)
