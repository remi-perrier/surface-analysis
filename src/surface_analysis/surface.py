from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from surface_analysis.transforms._base import Transformation


@dataclass
class Surface:
    z: NDArray[np.float64]  # (ny, nx) height map in mm
    step_x: float  # pixel spacing in mm
    step_y: float  # pixel spacing in mm

    def apply(self, *transforms: Transformation) -> Surface:
        result = self
        for t in transforms:
            result = t.transform(result)
        return result

    @classmethod
    def from_datx(cls, path: str) -> Surface:
        from surface_analysis.io import load_datx

        return load_datx(path)

    @classmethod
    def from_array(cls, z: NDArray, step_x: float, step_y: float) -> Surface:
        return cls(z=np.asarray(z, dtype=np.float64), step_x=step_x, step_y=step_y)

    @property
    def shape(self) -> tuple[int, int]:
        return self.z.shape

    @property
    def size_x(self) -> float:
        return self.z.shape[1] * self.step_x

    @property
    def size_y(self) -> float:
        return self.z.shape[0] * self.step_y

    @property
    def x(self) -> NDArray[np.floating]:
        return np.arange(self.z.shape[1]) * self.step_x

    @property
    def y(self) -> NDArray[np.floating]:
        return np.arange(self.z.shape[0]) * self.step_y

    @property
    def nan_count(self) -> int:
        return int(np.isnan(self.z).sum())

    @property
    def nan_ratio(self) -> float:
        return np.isnan(self.z).sum() / self.z.size

    # --- ISO 25178 height parameters ---

    @property
    def _valid(self) -> NDArray[np.float64]:
        return self.z[np.isfinite(self.z)]

    @property
    def Sa(self) -> float:
        v = self._valid
        return float(np.mean(np.abs(v - np.mean(v))))

    @property
    def Sq(self) -> float:
        v = self._valid
        return float(np.sqrt(np.mean((v - np.mean(v)) ** 2)))

    @property
    def Sp(self) -> float:
        v = self._valid
        return float(np.max(v) - np.mean(v))

    @property
    def Sv(self) -> float:
        v = self._valid
        return float(np.mean(v) - np.min(v))

    @property
    def Sz(self) -> float:
        return self.Sp + self.Sv

    @property
    def Ssk(self) -> float:
        v = self._valid
        mean = np.mean(v)
        sq = self.Sq
        if sq == 0:
            return 0.0
        return float(np.mean((v - mean) ** 3) / sq**3)

    @property
    def Sku(self) -> float:
        v = self._valid
        mean = np.mean(v)
        sq = self.Sq
        if sq == 0:
            return 0.0
        return float(np.mean((v - mean) ** 4) / sq**4)

    # --- ISO 25178 hybrid parameters ---

    @property
    def Sdq(self) -> float:
        z = self.z
        dzdx = np.gradient(z, self.step_x, axis=1)
        dzdy = np.gradient(z, self.step_y, axis=0)
        slope_sq = dzdx**2 + dzdy**2
        valid = slope_sq[np.isfinite(slope_sq)]
        return float(np.sqrt(np.mean(valid)))

    @property
    def Sdr(self) -> float:
        z = self.z
        dzdx = np.gradient(z, self.step_x, axis=1)
        dzdy = np.gradient(z, self.step_y, axis=0)
        local_area = np.sqrt(1 + dzdx**2 + dzdy**2)
        valid = local_area[np.isfinite(local_area)]
        return float((np.mean(valid) - 1) * 100)

    def parameters(self) -> dict[str, float]:
        return {
            "Sa": self.Sa,
            "Sq": self.Sq,
            "Sp": self.Sp,
            "Sv": self.Sv,
            "Sz": self.Sz,
            "Ssk": self.Ssk,
            "Sku": self.Sku,
            "Sdq": self.Sdq,
            "Sdr": self.Sdr,
        }

    def plot(self, **kwargs):
        from surface_analysis.viz import plot_surface

        return plot_surface(self, **kwargs)

    def __repr__(self) -> str:
        ny, nx = self.shape
        return (
            f"Surface({nx}x{ny}, "
            f"step=({self.step_x:.4f}, {self.step_y:.4f}) mm, "
            f"nan={self.nan_ratio:.1%})"
        )
