# surface-analysis

Analyze 3D surface topography from microscope measurements.
Decompose surfaces into form, waviness, roughness, and micro-roughness following ISO 25178 / ISO 16610.

## Install

```bash
uv add git+https://github.com/remi-perrier/surface-analysis
```

For development:

```bash
git clone https://github.com/remi-perrier/surface-analysis.git
cd surface-analysis
uv sync
```

## Quick start

```python
from surface_analysis import Surface

# Load and decompose in one call (ISO 25178-3 F/S/L pipeline)
dec = Surface.from_datx("measurement.datx").decompose(
    form="polynomial",       # form removal (plane or polynomial)
    lambda_c=0.8,            # waviness/roughness cutoff (mm)
    lambda_s=0.025,          # roughness/micro-roughness cutoff (mm)
    interpolation="nearest", # NaN filling method
)

# Access each layer
dec.form                # fitted polynomial form
dec.waviness            # wavelengths > 0.8 mm
dec.roughness           # wavelengths 0.025–0.8 mm (isolated bandpass)
dec.micro_roughness     # wavelengths < 0.025 mm

# ISO 25178 parameters on any layer
print(f"Sa = {dec.roughness.Sa * 1000:.2f} µm")
print(f"Ssk = {dec.roughness.Ssk:.3f}")
dec.roughness.parameters()  # dict with all 9 parameters
```

Without `lambda_s`, roughness contains everything below `lambda_c`:

```python
dec = surface.decompose(lambda_c=0.8)
dec.micro_roughness  # None
```

## Surface arithmetic

```python
# Verify decomposition reconstruction
reconstructed = dec.form + dec.waviness + dec.roughness + dec.micro_roughness

# Scale, negate, compare
diff = surface_a - surface_b
scaled = surface * 0.5
```

## Low-level transforms

For custom pipelines, use `apply()` with individual transforms:

```python
from surface_analysis import Transforms

roughness = (
    Surface.from_datx("measurement.datx")
    .apply(
        Transforms.Interpolation.Linear(),
        Transforms.Projection.Polynomial(degree=2),
        Transforms.Filtering.Gaussian(cutoff=0.8),
    )
)
```

## Visualization

```python
surface.plot()                  # 2D height map (matplotlib)
surface.plot_3d()               # 3D static view (matplotlib)
fig = surface.plot_3d_interactive()  # 3D interactive (plotly)
fig.write_html("output.html")
```

## Units

Everything is in **mm** internally. Multiply by 1000 for display in µm.
