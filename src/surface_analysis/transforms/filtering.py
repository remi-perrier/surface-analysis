from __future__ import annotations

from typing import Literal

import numpy as np
from scipy.ndimage import gaussian_filter

from surface_analysis.surface import Surface
from surface_analysis.transforms._base import Transformation

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
    def __init__(
        self, cutoff: float, mode: Literal["highpass", "lowpass"] = "highpass"
    ) -> None:
        if cutoff <= 0:
            raise ValueError(f"Cutoff must be positive, got {cutoff}")
        valid_modes = ("highpass", "lowpass")
        if mode not in valid_modes:
            raise ValueError(f"Mode must be one of {valid_modes}, got {mode!r}")
        self.cutoff = cutoff
        self.mode = mode

    def transform(self, surface: Surface) -> Surface:
        sigma_mm = self.cutoff * _ISO_SIGMA_FACTOR
        sigma_x_px = sigma_mm / surface.step_x
        sigma_y_px = sigma_mm / surface.step_y

        lowpass = _gaussian_filter_nan(surface.z, sigma_x_px, sigma_y_px)

        if self.mode == "lowpass":
            z_out = lowpass
        elif self.mode == "highpass":
            z_out = surface.z - lowpass
        else:
            raise ValueError(f"Unknown mode {self.mode!r}")

        return Surface(z=z_out, step_x=surface.step_x, step_y=surface.step_y)
