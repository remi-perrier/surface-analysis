# Surface Metrology Analysis - Subject Understanding

## Context

A physicist uses a microscope (likely confocal or interferometric) to measure the 3D topography
of a tube's surface. The instrument produces a height map z(x, y) representing surface height
at each measured position on a regular grid. The goal is to characterize **surface roughness** by
isolating it from other surface components (form, waviness, micro-roughness).

---

## 1. The 4 Surface Components

A measured surface is a superposition of features at different spatial wavelengths. The decomposition
is performed by progressively filtering out spectral bands:

```
Measured surface = Form + Waviness + Roughness + Micro-roughness
                   |         |          |            |
              Longest lambda               Shortest lambda
```

| Component           | Physical origin                          | Typical wavelengths           | Spatial frequency |
|---------------------|------------------------------------------|-------------------------------|-------------------|
| **Form**            | Macro geometry (cylinder, sphere, tilt)  | > lambda_f (typically > 0.8-8 mm) | Lowest |
| **Waviness**        | Machine vibrations, chatter, thermal drift | lambda_c to lambda_f          | Low-mid |
| **Roughness**       | Tool marks, grain structure, process marks | lambda_s to lambda_c          | Mid-high |
| **Micro-roughness** | Instrument noise, sub-resolution features | < lambda_s (typically < 2.5-8 um) | Highest |

**Key principle**: the boundaries between components are NOT fixed physical constants. They depend
on the application and on the measurement instrument. The cutoff wavelengths must be chosen based
on what features are functionally relevant.

### Standard Cutoff Wavelengths

Three cutoff wavelengths define the spectral decomposition:

- **lambda_s** (S-filter): separates micro-roughness from roughness.
  - Physically motivated by the stylus tip radius (contact instruments) or optical resolution limit.
  - ISO 3274 standard values: 2.5 um (for 2 um tip radius) or 8 um (for 5 um or 10 um tip radius).
  - For optical instruments (confocal, interferometry), lambda_s is set to ~3x the lateral pixel spacing.
  - Standard bandwidth ratio: **lambda_c / lambda_s = 300** (ISO convention, ISO 4288).

- **lambda_c** (roughness cutoff / L-filter): separates roughness from waviness.
  - Standard series (ISO 4288 / ISO 21920-3): **0.08, 0.25, 0.8, 2.5, 8.0 mm**
  - Choice depends on expected Ra (see cutoff selection table below).

- **lambda_f** (F-operator): separates waviness from form.
  - Not a filter in the classical sense; form removal uses geometric fitting (least squares).
  - For areal (ISO 25178), the F-operator is a form fitting/subtraction step, not a wavelength filter.

### ISO 4288 Cutoff Selection Table (Non-Periodic Profiles)

This table from ISO 4288:1996 (now replaced by ISO 21920-3) links expected Ra to the recommended
cutoff lambda_c and evaluation length:

| Ra range (um)       | lambda_c (mm) | Sampling length (mm) | Evaluation length (mm) |
|---------------------|---------------|----------------------|------------------------|
| 0.006 < Ra <= 0.02  | 0.08          | 0.08                 | 0.4                    |
| 0.02 < Ra <= 0.1    | 0.25          | 0.25                 | 1.25                   |
| 0.1 < Ra <= 2       | 0.8           | 0.8                  | 4.0                    |
| 2 < Ra <= 10        | 2.5           | 2.5                  | 12.5                   |
| 10 < Ra <= 80       | 8.0           | 8.0                  | 40.0                   |

For periodic profiles (e.g., turned surfaces), ISO 4288 Table 3 uses RSm (mean spacing) instead of Ra.

**Note on ISO 21920**: Since December 2022, ISO 21920 replaces ISO 4287, ISO 4288, ISO 1302, and
ISO 13565. Under ISO 21920, parameters (Ra, Rq) are computed over the entire evaluation length
rather than averaged over 5 sampling lengths. Default measurement conditions are defined in
ISO 21920-3, reducing user-dependent variation.

### Recommended Nesting Index Values for Areal Surfaces (ISO 25178-3)

For areal (3D) measurements, the recommended S-filter and L-filter nesting index series is:

**S-filter**: 0.5, 1, 2, 2.5, 5, 8, 10, 20, 25 um (application-dependent, typically 2.5 um)

**L-filter**: 0.1, 0.2, 0.25, 0.5, 0.8, 1.0 mm (and beyond)

---

## 2. Relevant ISO Standards

### ISO 25178 - Areal Surface Texture

The primary standard for 3D surface texture analysis. Multi-part structure:

| Part | Title | Content |
|------|-------|---------|
| 25178-1 | Indication of surface texture | Drawing specifications for areal parameters |
| 25178-2 | Terms, definitions and parameters | **Core**: defines all S-parameters (Sa, Sq, Ssk, Sku, Sdq, Sdr, Sal, Str, etc.) |
| 25178-3 | Specification operators | Default nesting index values, evaluation rules, extraction methods |
| 25178-6 | Classification of methods | Taxonomy of measurement instrument types |
| 25178-70 | Material measures | Defines calibration artefacts for areal instruments |
| 25178-600 | Metrological characteristics | Unified framework for instrument performance |
| 25178-601 | Nominal characteristics of contact instruments | Stylus-based areal measurement |
| 25178-602 | Nominal characteristics of non-contact (confocal chromatic) | Confocal chromatic probe instruments |
| 25178-603 | Nominal characteristics of non-contact (phase-shifting interferometric) | PSI instruments |
| 25178-604 | Nominal characteristics of non-contact (coherence scanning interferometric) | CSI / white-light interferometry |
| 25178-605 | Nominal characteristics of non-contact (point autofocus) | Point autofocus instruments |
| 25178-606 | Nominal characteristics of non-contact (focus variation) | Focus variation instruments (e.g., Alicona) |
| 25178-607 | Nominal characteristics of non-contact (confocal) | Confocal microscopes (laser scanning) |
| 25178-700 | Calibration | Calibration of metrological characteristics |
| 25178-701 | Calibration of contact instruments | Stylus calibration procedures |
| 25178-71 | Software measurement standards (SDF) | Surface Data File format for softgauges |
| 25178-72 | XML softgauge format (S3P) | XML-based data exchange format |

**Current version**: ISO 25178-2:2021 (revised from 2012 edition, adds corrections and new parameters).

### ISO 16610 - Filtration

The comprehensive standard for all filter types used in surface metrology:

| Part | Filter type | Domain |
|------|-------------|--------|
| **Linear profile filters** | | |
| 16610-20 | Basic concepts | Profile |
| 16610-21 | Gaussian filters | Profile |
| 16610-22 | Spline filters | Profile |
| 16610-28 | End effects | Profile |
| 16610-29 | Spline wavelets | Profile |
| **Robust profile filters** | | |
| 16610-30 | Basic concepts | Profile |
| 16610-31 | Gaussian regression filters | Profile |
| 16610-32 | Spline filters | Profile |
| **Morphological profile filters** | | |
| 16610-40 | Basic concepts | Profile |
| 16610-41 | Disk and horizontal segment filters | Profile |
| 16610-42 | Motif filters | Profile |
| 16610-49 | Scale space techniques | Profile |
| **Linear areal filters** | | |
| 16610-60 | Basic concepts | Areal |
| 16610-61 | Gaussian filters | Areal |
| 16610-62 | Spline filters | Areal |
| 16610-69 | Spline wavelets | Areal |
| **Robust areal filters** | | |
| 16610-70 | Basic concepts | Areal |
| 16610-71 | Gaussian regression filters | Areal |
| 16610-72 | Spline filters | Areal |
| **Morphological areal filters** | | |
| 16610-80 | Basic concepts | Areal |
| 16610-81 | Sphere and horizontal planar segment filters | Areal |
| 16610-82 | Motif filters | Areal |
| 16610-89 | Scale space techniques | Areal |

### ISO 4287 / ISO 21920 - Profile Parameters

- **ISO 4287:1997** (withdrawn 2021): Defined Ra, Rq, Rz, Rsk, Rku, RSm, etc. for profiles.
- **ISO 4288:1996** (withdrawn 2021): Rules for cutoff selection (the Ra vs lambda_c tables).
- **ISO 21920-2:2022**: Replaces ISO 4287, broadens parameter definitions.
- **ISO 21920-3:2022**: Replaces ISO 4288, defines default measurement conditions.

### Other Relevant Standards

- **ISO 3274:1996**: Contact instrument nominal characteristics (stylus tip radius: 2, 5, or 10 um; cone angle: 60 or 90 deg).
- **ISO 12085**: Motif parameters (R, W motifs).
- **ISO 13565-2/-3**: Stratified surface parameters (Rk, Rpk, Rvk). Now in ISO 21920-2.

---

## 3. Filtering Methods

### 3.1 Gaussian Filter (ISO 16610-21 / 16610-61)

The **default** filter in surface metrology. Defined by a Gaussian weighting function applied
via convolution.

**Weighting function** (1D profile):

```
h(x) = (alpha / lambda_c) * (1/sqrt(pi)) * exp(-(alpha * x / lambda_c)^2)
```

where **alpha = sqrt(ln(2)/pi) = 0.4697** is chosen so that the transmission at wavelength
lambda_c is exactly **50%**.

**Transfer function** in frequency domain:

```
H(f) = exp(-pi * (f * lambda_c / alpha)^2)
```

At the cutoff spatial frequency f_c = 1/lambda_c, the amplitude transmission is 50%.

**Characteristics:**
- Smooth, symmetric weighting (no phase distortion).
- At cutoff: 50% amplitude transmission (not a sharp brick-wall filter).
- Applied via convolution in spatial domain or multiplication in Fourier domain.
- **End effects**: the Gaussian filter distorts results near profile/surface boundaries by
  approximately 0.5 to 1 cutoff length on each side. Manufacturers typically discard 0.6-2
  cutoff lengths from filtered edges.
- The Gaussian filter is a linear filter: components of different wavelengths are processed
  independently (no cross-talk).

**Robust Gaussian regression filter** (ISO 16610-31/71): uses iterative reweighting to reduce
sensitivity to outliers (spikes, deep scratches). The weighting function assigns low weights
to outliers and zero weight to dropouts/NaN.

### 3.2 Spline Filter (ISO 16610-22 / 16610-62)

A cubic spline filter that connects data points through a mechanical analogy: suspended masses
connected to the original data via springs with a tension parameter beta.

**Key property**: when beta = 0.6252, the spline filter behavior is numerically very close to
the Gaussian filter.

**Advantages over Gaussian:**
- **No end effects**: the spline naturally handles profile boundaries without distortion. This
  is its primary practical advantage.
- **Efficient computation**: O(n) via tridiagonal matrix solving, or O(n log n) via DCT/FFT
  implementation. The Gaussian convolution is O(n * m) where m is the kernel size.
- **Form-following capability**: can follow slowly varying form errors better.

**Robust spline filter** (ISO 16610-32/72): incorporates iterative reweighting for outlier
insensitivity, similar to the robust Gaussian. A weighting function gives outliers low weight
and dropouts zero weight.

### 3.3 Morphological Filters (ISO 16610-41 / 16610-81)

Non-linear filters based on mathematical morphology. Instead of weighted averaging, they use
a **structuring element** (disk in 2D, sphere in 3D) that rolls along the surface.

**Four basic operations:**

| Operation | Definition | Effect |
|-----------|-----------|--------|
| **Dilation** | Structuring element slides on top; take upper boundary | Enlarges peaks, fills valleys |
| **Erosion** | Structuring element slides below; take lower boundary | Deepens valleys, removes peaks |
| **Closing** | Dilation then erosion | **Upper envelope**: follows peaks, bridges valleys |
| **Opening** | Erosion then dilation | **Lower envelope**: follows valleys, truncates peaks |

**Physical interpretation**: the closing filter places a disk (or sphere) of given radius in
contact with the surface from above and traces its lowest point. The opening filter does the
same from below. The structuring element size defines the "nesting index" (analogous to cutoff
wavelength for linear filters).

**Use cases:**
- Functional surface analysis (plateau honing: bearing surface vs. oil retention valleys).
- Envelope-based roughness (contact area estimation).
- When the standard Gaussian filter gives misleading results on surfaces with deep scratches
  or steep features.

**Important**: morphological filters are non-linear, so the concept of "cutoff wavelength" does
not strictly apply. Instead, ISO 16610 uses the term **nesting index** for the structuring
element radius.

### 3.4 Filter Chain (ISO 25178 Evaluation Pipeline)

The complete processing chain for areal surface texture analysis:

```
Raw measurement
     |
     v
[S-filter (lambda_s)] ----> Removes micro-roughness / instrument noise
     |                       Output: Primary surface
     v
[F-operator] ------------> Removes form (geometric fitting & subtraction)
     |                       Output: S-F surface (scale-limited surface for roughness)
     v
[L-filter (lambda_c)] ---> Separates remaining content into roughness and waviness
     |                       Output: S-L surface (scale-limited surface for waviness)
     v
  Parameters computed on S-F surface (roughness) or S-L surface (waviness)
```

**S-F surface**: primary surface after S-filter and F-operator. Used for computing roughness
parameters (Sa, Sq, etc.) when no L-filter is needed (common case for microscope data where
the field of view is small relative to waviness wavelengths).

**S-L surface**: primary surface after S-filter and L-filter (no F-operator). Used for computing
waviness parameters. The L-filter acts as the long-wavelength cutoff.

**Practical guidance for S-filter nesting index**: set to >= 3x the lateral pixel spacing
of the measurement. For example, if pixel spacing is 1 um, use lambda_s >= 3 um.

**Practical guidance for L-filter nesting index**: set to <= 1/5 of the measurement field
dimension (ensures at least 5 wavelengths fit in the measured area for statistical significance).

---

## 4. Surface Texture Parameters

### 4.1 Profile Parameters (ISO 4287 / ISO 21920-2)

Defined on a 2D profile z(x) after filtering. Prefix R = roughness profile, W = waviness
profile, P = primary profile.

#### Height parameters

**Ra** (Arithmetic mean deviation):
```
Ra = (1/L) * integral_0^L |z(x)| dx
```
Discrete: Ra = (1/N) * sum_{i=1}^{N} |z_i|. Most common parameter, but insensitive to
spatial structure (a periodic and random surface can have identical Ra).

**Rq** (Root mean square deviation):
```
Rq = sqrt((1/L) * integral_0^L z(x)^2 dx)
```
For a Gaussian height distribution: Ra ~ 0.8 * Rq. Rq is the standard deviation of the
height distribution (assuming zero mean after filtering).

**Rz** (Maximum height of profile):
```
Rz = Rp + Rv = max(z) - min(z)    (within evaluation length)
```
In ISO 4287: Rz = average of 5 highest peaks + 5 deepest valleys (ten-point height).
In ISO 21920: Rz = Rp + Rv (maximum peak-to-valley, simpler definition).

**Rsk** (Skewness):
```
Rsk = (1/Rq^3) * (1/L) * integral_0^L z(x)^3 dx
```
Rsk = 0: symmetric distribution. Rsk < 0: dominated by valleys (plateau-like surface,
good for bearing). Rsk > 0: dominated by peaks (spiky surface).

**Rku** (Kurtosis):
```
Rku = (1/Rq^4) * (1/L) * integral_0^L z(x)^4 dx
```
Rku = 3: Gaussian distribution. Rku > 3: sharp peaks/valleys (leptokurtic).
Rku < 3: broad, flat distribution (platykurtic).

### 4.2 Areal Parameters (ISO 25178-2)

Defined on a 2D height map z(x, y) over a definition area A. These are the primary
parameters for microscope-based surface analysis.

#### Height Parameters

**Sa** (Arithmetical mean height):
```
Sa = (1/A) * double_integral_A |z(x,y)| dA
```
3D extension of Ra. General-purpose parameter, widely used but insensitive to spatial layout.

**Sq** (Root mean square height):
```
Sq = sqrt((1/A) * double_integral_A z(x,y)^2 dA)
```
Standard deviation of the height distribution. For Gaussian surfaces: Sa ~ 0.8 * Sq.

**Sp** (Maximum peak height):
```
Sp = max(z(x,y))     over A
```

**Sv** (Maximum valley depth):
```
Sv = |min(z(x,y))|   over A
```

**Sz** (Maximum height):
```
Sz = Sp + Sv = max(z) - min(z)
```
Sensitive to outliers/spikes. Consider Sz after outlier removal.

**Ssk** (Skewness):
```
Ssk = (1/Sq^3) * (1/A) * double_integral_A z(x,y)^3 dA
```
Same interpretation as Rsk. Ssk < 0: surface dominated by valleys (plateau honed surfaces).
Ssk > 0: surface dominated by peaks.

**Sku** (Kurtosis):
```
Sku = (1/Sq^4) * (1/A) * double_integral_A z(x,y)^4 dA
```
Sku = 3 for Gaussian. Sku > 3: sharp features. Sku < 3: broad features.

#### Hybrid Parameters

**Sdq** (Root mean square gradient):
```
Sdq = sqrt((1/A) * double_integral_A [(dz/dx)^2 + (dz/dy)^2] dA)
```
Measures local slope complexity. Expressed in um/um or dimensionless. Higher Sdq means
steeper local slopes and more complex texture. Useful for distinguishing surfaces with
similar Sa but different morphology.

**Sdr** (Developed interfacial area ratio):
```
Sdr = (A_real - A_projected) / A_projected * 100%
```
where A_real is the true (curvilinear) surface area computed by triangulating the height map,
and A_projected is the flat projected area. Sdr = 0% for a perfectly flat surface. Sdr is
related to fractal dimension and scale-sensitive analysis.

#### Spatial Parameters

**Sal** (Autocorrelation length):
```
Sal = min(r) such that ACF(r) <= s     for all directions
```
where ACF is the areal autocorrelation function and s = 0.2 (default threshold). Sal is
the shortest distance over which the autocorrelation drops below s. Small Sal = steep,
rapidly varying texture. Large Sal = slowly varying, smooth texture.

**Str** (Texture aspect ratio):
```
Str = Sal / Sar
```
where Sar is the slowest decay autocorrelation length (maximum distance where ACF stays
above s). Str ranges from 0 to 1:
- Str > 0.5: isotropic (similar texture in all directions).
- Str < 0.3: strongly anisotropic (directional texture, e.g., turning marks).

**Std** (Texture direction):
Dominant direction of surface lay, determined from the angular spectrum (Fourier transform
modulus in polar coordinates). Expressed in degrees anticlockwise from the x-axis.

#### Functional Parameters (ISO 25178-2)

Based on the Abbott-Firestone (bearing ratio) curve:

**Smr(c)** (Areal material ratio): fraction of surface above a given height c.

**Smc(mr)** (Inverse areal material ratio): height at which the material ratio equals mr.

**Sxp** (Extreme peak height): height difference between the material ratio levels p% and q%
(default: between 2.5% and 50%). Related to peak-to-core height.

#### Functional Volume Parameters (Sk family, from ISO 13565-2)

**Sk** (Core roughness depth): height of the core region of the bearing ratio curve.

**Spk** (Reduced peak height): mean height of protruding peaks above the core.

**Svk** (Reduced valley depth): mean depth of valleys below the core.

**Smr1, Smr2**: material ratios at the boundaries of the core region.

These are critical for functional analysis: Spk relates to initial running-in wear,
Sk to long-term bearing, Svk to lubricant retention capacity.

---

## 5. Tube Surface Specifics: Cylindrical Geometry

### The Problem

When measuring the inner or outer surface of a tube with an optical microscope, the measured
height map z(x, y) contains a large cylindrical curvature component that dominates all texture
features. This curvature is the **form** and must be removed before roughness analysis.

If the tube radius is R and the measurement covers a small arc, the cylindrical form appears
approximately parabolic in the height map (for small arcs relative to R).

### Form Removal Approaches

#### Least-Squares Cylinder Fitting (Standard Approach)

1. **Model**: The cylinder surface is described by (x - x0)^2 + (z - z0)^2 = R^2 with axis
   along y. Parameters to fit: center (x0, z0), radius R, and potentially axis orientation
   (tilt angles theta_x, theta_y).

2. **Algorithm**:
   - For a known axis direction: project data onto a plane perpendicular to the axis, then fit
     a circle using Pratt's method or Taubin's method (algebraic least squares). These methods
     are more numerically stable than geometric least squares for partial arcs.
   - For an unknown axis: first estimate the axis direction (e.g., via PCA on the point cloud
     or by fitting planes to cross-sections), then iterate cylinder fitting.
   - Least-squares (L2-norm) association: minimize sum of squared radial residuals.

3. **Subtraction**: Compute radial residual for each point:
   ```
   residual_i = sqrt((x_i - x0)^2 + (z_i - z0)^2) - R
   ```
   The residual map contains waviness + roughness + micro-roughness.

4. **Coordinate transformation**: For small arcs, the residuals can be mapped back to a flat
   (x, y) grid. For larger arcs, unroll the cylinder: convert to cylindrical coordinates
   (theta, y, r) where theta = atan2(x - x0, z - z0), and the residual becomes delta_r(theta, y).

#### Polynomial Fitting (Alternative)

For a small field of view relative to the tube radius, the cylindrical form is well approximated
by a 2nd-order polynomial:

```
z_form(x, y) = a00 + a10*x + a01*y + a20*x^2 + a11*x*y + a02*y^2
```

Fit by least squares, then subtract. Higher-order polynomials (degree 3-6) can absorb
waviness, which may not be desired unless intentional.

**Warning**: polynomials diverge at edges, especially at high order. For tube surfaces,
cylinder fitting is always preferred over polynomial fitting when the geometry is known.

#### Minimum Zone Method (L-infinity)

Encloses the surface between two concentric cylinders of minimum radial separation. Used in
dimensional metrology (roundness evaluation) more than in roughness analysis.

### Practical Considerations for Tube Measurements

- **Field of view**: if the microscope measures a flat-looking patch (FOV << tube diameter),
  the cylinder appears as a gentle parabola. A 2nd-order polynomial may suffice.
- **Stitching**: for larger coverage, multiple fields are stitched. The stitched map will show
  more curvature and requires proper cylinder fitting.
- **Axis alignment**: the tube axis should be approximately aligned with one measurement axis
  (typically y). Misalignment adds a tilt component that must be included in the fitting model.
- **Confocal unrolling**: some instruments (e.g., Sensofar with a rotation stage) can acquire
  unrolled cylindrical measurements directly by rotating the tube and stitching angular fields.

---

## 6. Interpolation Methods for Missing Data

### Why Missing Data Occurs

Optical microscopes (confocal, interferometric) produce **non-measured points** (NaN/void) when:
- Local surface slopes exceed the instrument's numerical aperture (steep flanks).
- Low reflectivity areas (dark materials, transparent coatings).
- Shadowing effects in the optical path.
- Multiple reflections or fringe order ambiguity (interferometry).
- Surface contamination (dust, debris).

Typical non-measured point fractions: 1-30% depending on surface complexity.

### Treatment Options

There are two philosophies:

1. **Exclude NaN from calculations**: algorithms must handle sparse data. Some parameters
   (Sa, Sq) can be computed by averaging only valid points. But gradient-based parameters
   (Sdq, Sdr) and filters requiring neighbors become problematic.

2. **Fill/interpolate NaN before analysis**: replace non-measured points with estimated values,
   then apply standard algorithms on the complete grid. This is the more common approach in
   professional software.

### Interpolation Methods

#### Nearest-Neighbor Interpolation
- Replace each NaN with the value of the closest valid pixel.
- Fast, O(n) with a distance transform.
- Produces blocky artifacts; discontinuous at boundaries.
- Acceptable for isolated missing points but poor for large voids.

#### Bilinear / Bicubic Interpolation
- Interpolate using the 4 (bilinear) or 16 (bicubic) nearest valid neighbors.
- Smooth result, C^0 (bilinear) or C^1 (bicubic) continuity.
- Standard in image processing. Works well for small voids.
- Fails for large contiguous missing regions.

#### Thin-Plate Spline (TPS) Interpolation
- Minimizes the bending energy functional:
  ```
  E = double_integral [(d^2z/dx^2)^2 + 2(d^2z/dxdy)^2 + (d^2z/dy^2)^2] dA
  ```
- Produces an infinitely differentiable surface (C^infinity).
- Physically motivated: mimics a thin elastic plate forced through known data points.
- Can produce overshoots near sharp transitions.
- Computationally expensive for large datasets: O(n^3) for direct solve.
- Regularized variant (with tension parameter) allows tuning between smooth interpolation
  and flatter behavior.

#### Laplacian / Biharmonic Interpolation (Smooth Pasting)
- Solves the Laplace equation (nabla^2 z = 0) or biharmonic equation (nabla^4 z = 0) in
  the missing regions, using valid data as Dirichlet boundary conditions.
- Laplacian: C^0 at boundaries, smooth interior. Equivalent to a membrane stretched over
  the void.
- Biharmonic: C^1 at boundaries (matching both value and gradient). Smoother result,
  equivalent to a thin plate.
- Standard in MATLAB (`regionfill`, `inpaint_nans`), available in scipy.
- Good balance of smoothness and computational cost.
- Recommended for surface metrology as it does not introduce artificial texture.

#### Kriging (Geostatistical)
- Uses a variogram model to account for spatial correlation in the data.
- Optimal linear unbiased estimator (BLUE) under the variogram model assumptions.
- Can account for heterogeneous measurement errors.
- More complex to implement; requires variogram estimation.
- Overkill for surface metrology unless the spatial correlation structure is specifically of interest.

### Recommended Approach for Surface Topography

1. **Small voids (< 5x5 pixels)**: bilinear or bicubic interpolation.
2. **Medium voids**: Laplacian/biharmonic interpolation (smooth pasting).
3. **Large voids (> 10% of field)**: consider excluding the region rather than interpolating.
   Interpolated areas should NOT contribute to parameter calculation.
4. Professional software (Digital Surf MountainsMap) uses a combination: smooth pasting for
   small/medium voids, with options for TPS and nearest-neighbor.
5. **Always document** which interpolation was used and what fraction of data was interpolated,
   as this affects measurement uncertainty.

---

## 7. Mathematical Details of the Gaussian Filter

### 1D Profile Gaussian Filter

**Weighting function**:
```
s(x) = (1 / (alpha * lambda_c * sqrt(2*pi))) * exp(-pi * (x / (alpha * lambda_c))^2)
```

where alpha = sqrt(ln(2)/pi) ~ 0.4697.

**Convolution for the mean line (waviness)**:
```
w(x) = integral_{-inf}^{+inf} s(t) * z(x - t) dt
```

**Roughness**:
```
r(x) = z(x) - w(x)
```

### 2D Areal Gaussian Filter (ISO 16610-61)

For isotropic filtering, the 2D weighting function is a product of two 1D Gaussians:

```
s(x, y) = s_x(x) * s_y(y)
```

with the same alpha and lambda_c in both directions (isotropic case). Anisotropic filtering
uses different cutoffs in x and y.

### Discrete Implementation

In practice, the convolution is performed discretely:
```
w[i] = sum_{k=-M}^{M} s[k] * z[i-k]    where M ~ 3 * lambda_c / dx
```
The kernel is truncated at ~3 cutoff lengths (where the weight drops to <0.3% of peak).

**FFT implementation**: For large datasets, compute via FFT:
1. FFT(z), FFT(s)
2. Multiply in frequency domain
3. Inverse FFT

This is O(N log N) vs O(N * M) for direct convolution.

---

## 8. Data Format: DATAX (.datx)

The `.datx` format is an **HDF5-based format from Zygo** (used with MetroPro/Mx software).
It stores surface topography data with metadata (measurement parameters, instrument info).

- Can be read with `h5py` in Python.
- Structure: hierarchical groups containing datasets (height map, intensity, phase...).
- A community gist exists for parsing: https://gist.github.com/g-s-k/ccffb1e84df065a690e554f4b40cfd3a
- Other instrument makers (Bruker, Keyence, Alicona) have their own formats, but if the user
  confirms HDF5/DATAX, we target Zygo format first.

---

## References and Sources

- [Digital Surf - Surface Metrology Guide: Filtration Techniques](https://guide.digitalsurf.com/en/guide-filtration-techniques.html)
- [Digital Surf - Surface Metrology Guide: Areal Field Parameters](https://guide.digitalsurf.com/en/guide-areal-field-parameters.html)
- [Digital Surf - Surface Metrology Guide: Leveling and Form Removal](https://guide.digitalsurf.com/en/guide-leveling-form-removal.html)
- [Digital Surf - Surface Metrology Guide: Micro-roughness Filter](https://guide.digitalsurf.com/en/guide-lambdas-filter.html)
- [Digital Surf - Surface Metrology Guide: ISO 25178 Structure](https://guide.digitalsurf.com/en/guide-iso-25178-structure.html)
- [Digital Surf - Surface Metrology Guide: Profile Parameters](https://guide.digitalsurf.com/en/guide-profile-parameters.html)
- [Digital Surf - Differences between ISO 4287 and ISO 21920](https://www.digitalsurf.com/blog/what-are-the-differences-between-iso-4287-and-iso-21920/)
- [Digital Metrology - 3 Steps to Understanding Surface Texture](https://digitalmetrology.com/tutorials/3-steps-to-understanding-surface-texture/)
- [Digital Metrology - Gaussian Filters Basics](https://digitalmetrology.com/tutorials/gaussian-filters-basics/)
- [Michigan Metrology - Form, Waviness and Roughness](https://michmet.com/take-a-hike-understanding-form-waviness-and-roughness-in-terms-of-a-good-walk/)
- [KEYENCE - Evaluation Process and Filtering (ISO 25178)](https://www.keyence.com/ss/products/microscope/roughness/surface/evaluation_process.jsp)
- [KEYENCE - Measurement Procedure (ISO 4288)](https://www.keyence.com/ss/products/microscope/roughness/line/measurement_procedure.jsp)
- [NIST - A Simple and Fast Spline Filtering Algorithm](https://nvlpubs.nist.gov/nistpubs/jres/120/jres.120.010.pdf)
- [PTB - Selected Filtration Methods of ISO 16610](https://www.ptb.de/cms/fileadmin/internet/fachabteilungen/abteilung_5/5.1_oberflaechenmesstechnik/DKD-Richtlinien/Selected_Filtration_Methods_of_ISO-16610.pdf)
- [Sensofar - Confocal Unrolled Areal Measurements of Cylindrical Surfaces](https://www.sensofar.com/pub-confocal-unrolled-areal-measurements-cylindrical-surfaces/)
- [Sensofar - ISO 25178 Standard](https://www.sensofar.com/metrology/technology/iso-25178-standard/)
- [Gear Solutions - Changes Ahead in Roughness Standards (ISO 21920)](https://gearsolutions.com/departments/materials-matter/changes-ahead-in-the-roughness-standards/)
- [CMM Quarterly - Understanding ISO 21920](https://cmm-quarterly.squarespace.com/articles/evolving-roughness-standards-understanding-and-implementing-iso-21920)
