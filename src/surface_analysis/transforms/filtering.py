from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from scipy.ndimage import gaussian_filter

from surface_analysis.transforms._base import Transformation

if TYPE_CHECKING:
    from surface_analysis.surface import Surface

# ISO 16610-21: sigma = cutoff * sqrt(ln2 / (2 * pi^2))
# At the cutoff wavelength, the Gaussian transmits 50% amplitude.
_ISO_SIGMA_FACTOR = float(np.sqrt(np.log(2) / (2 * np.pi**2)))


def _gaussian_filter_nan(z: np.ndarray, sigma_x: float, sigma_y: float) -> np.ndarray:
    mask = np.isfinite(z)
    z_zero = np.where(mask, z, 0.0)
    weights = mask.astype(np.float64)

    filtered = gaussian_filter(z_zero, sigma=[sigma_y, sigma_x])
    weight_filtered = gaussian_filter(weights, sigma=[sigma_y, sigma_x])

    result = np.where(weight_filtered > 0, filtered / weight_filtered, np.nan)
    return result


class Gaussian(Transformation):
    def __init__(self, cutoff: float, mode: str = "highpass"):
        self.cutoff = cutoff
        self.mode = mode

    def transform(self, surface: Surface) -> Surface:
        from surface_analysis.surface import Surface

        sigma_mm = self.cutoff * _ISO_SIGMA_FACTOR
        sigma_x_px = sigma_mm / surface.step_x
        sigma_y_px = sigma_mm / surface.step_y

        lowpass = _gaussian_filter_nan(surface.z, sigma_x_px, sigma_y_px)

        if self.mode == "lowpass":
            z_out = lowpass
        elif self.mode == "highpass":
            z_out = surface.z - lowpass
        else:
            raise ValueError(
                f"Unknown mode: {self.mode!r}. Use 'lowpass' or 'highpass'."
            )

        return Surface(z=z_out, step_x=surface.step_x, step_y=surface.step_y)
