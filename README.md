# surface-analysis

Analyze 3D surface topography from microscope measurements.
Extract roughness, waviness, and form from height maps following ISO 25178.

## Install

```bash
uv sync
```

## Quick start

```python
from surface_analysis import Surface, Transforms

# Load a Zygo .datx measurement
surface = Surface.from_datx("measurement.datx")

# Process: fill missing points, remove tube curvature, extract roughness
roughness = surface.apply(
    Transforms.interpolation.Linear(),
    Transforms.projection.Polynomial(degree=2),
    Transforms.filtering.Gaussian(cutoff=0.8),
)

# Read ISO 25178 parameters directly
print(f"Sa = {roughness.Sa * 1000:.2f} µm")
print(f"Sq = {roughness.Sq * 1000:.2f} µm")
print(f"Ssk = {roughness.Ssk:.3f}")

# Or get everything at once
roughness.parameters()
# {'Sa': 0.00707, 'Sq': 0.0093, 'Ssk': 1.146, 'Sku': 7.06, ...}
```

## Available transforms

| Category | Transform | Description |
|----------|-----------|-------------|
| **Interpolation** | `Linear()` | Fill NaN with linear interpolation |
| | `Nearest()` | Fill NaN with nearest neighbor |
| **Projection** | `Polynomial(degree=2)` | Remove form by polynomial fit |
| | `Plane()` | Remove tilt (degree 1) |
| **Filtering** | `Gaussian(cutoff=0.8)` | ISO 16610-21 Gaussian, highpass (roughness) |
| | `Gaussian(cutoff=0.8, mode="lowpass")` | Lowpass (waviness) |

All transforms satisfy the `Transformation` protocol and are composable via `surface.apply()`.

## Units

Everything is in **mm** internally. Multiply by 1000 for µm display.
