from __future__ import annotations

from typing import TYPE_CHECKING

import h5py
import numpy as np

if TYPE_CHECKING:
    from surface_analysis.surface import Surface


def load_datx(path: str) -> Surface:
    from surface_analysis.surface import Surface

    with h5py.File(path, "r") as f:
        surface_group = f["Data/Surface"]
        key = list(surface_group.keys())[0]
        ds = surface_group[key]

        z_raw = ds[()].astype(np.float64)

        # Spatial steps from converter attributes (stored in meters)
        step_x_m = ds.attrs["X Converter"][0][2][1]
        step_y_m = ds.attrs["Y Converter"][0][2][1]

        # No-data sentinel
        nodata = ds.attrs.get("No Data", [np.inf])[0]

    # Mask invalid values
    z_raw[np.isclose(z_raw, nodata) | (z_raw > 1e20)] = np.nan

    # Convert: raw is in nm, we store in mm
    z_mm = z_raw * 1e-6
    step_x_mm = float(step_x_m * 1e3)
    step_y_mm = float(step_y_m * 1e3)

    return Surface(z=z_mm, step_x=step_x_mm, step_y=step_y_mm)


def generate_synthetic(
    nx: int = 1000,
    ny: int = 1000,
    step: float = 0.001,  # 1 µm in mm
    radius: float = 5.0,  # tube radius in mm
    waviness_amplitude: float = 0.002,  # 2 µm in mm
    waviness_wavelength: float = 0.5,  # mm
    roughness_rms: float = 0.0003,  # 0.3 µm in mm
    noise_rms: float = 0.00005,  # 0.05 µm in mm
    seed: int | None = 42,
) -> Surface:
    from surface_analysis.surface import Surface

    rng = np.random.default_rng(seed)

    x = np.arange(nx) * step
    y = np.arange(ny) * step
    X, Y = np.meshgrid(x, y)

    # Form: cylindrical curvature (parabolic approximation for small arc)
    x_center = x[-1] / 2
    form = (X - x_center) ** 2 / (2 * radius)

    # Waviness: sinusoidal
    waviness = waviness_amplitude * np.sin(2 * np.pi * X / waviness_wavelength)

    # Roughness: correlated Gaussian noise
    from scipy.ndimage import gaussian_filter

    raw_noise = rng.standard_normal((ny, nx))
    correlation_px = 10  # pixels
    roughness = gaussian_filter(raw_noise, sigma=correlation_px)
    roughness = roughness / np.std(roughness) * roughness_rms

    # Micro-roughness: white noise
    noise = rng.standard_normal((ny, nx)) * noise_rms

    z = form + waviness + roughness + noise

    return Surface(z=z, step_x=step, step_y=step)
