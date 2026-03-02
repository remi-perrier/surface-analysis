from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


def _argclosest(array: NDArray, value: float) -> int:
    return int(np.argmin(np.abs(array - value)))


@dataclass
class AbbottFirestone:
    """ISO 13565-2 / ISO 25178-2 bearing area curve and derived parameters.

    Parameters
    ----------
    height : NDArray
        Height values (descending) of the material ratio curve.
    material_ratio : NDArray
        Material ratio values (ascending, 0 to 100 %) of the curve.
    """

    height: NDArray[np.float64]
    material_ratio: NDArray[np.float64]

    # --- Cached equivalent line results ---
    _eq_slope: float | None = None
    _eq_intercept: float | None = None

    @classmethod
    def from_surface(
        cls, z: NDArray[np.float64], n_bins: int = 10_000
    ) -> AbbottFirestone:
        """Build the material ratio curve from a height map.

        Parameters
        ----------
        z : NDArray
            2D height map. NaN values are excluded.
        n_bins : int
            Number of histogram bins.
        """
        valid = z[np.isfinite(z)]
        if valid.size == 0:
            raise ValueError("Cannot compute Abbott-Firestone: no valid points")

        z_min, z_max = float(np.min(valid)), float(np.max(valid))
        counts, bin_edges = np.histogram(valid, bins=n_bins, range=(z_min, z_max))

        # Material ratio curve: cumulate from highest to lowest
        # bin_centers from high to low
        bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
        height = bin_centers[::-1]
        cumulative = np.cumsum(counts[::-1])
        material_ratio = cumulative / valid.size * 100.0

        return cls(height=height, material_ratio=material_ratio)

    # --- Interpolation helpers ---

    def Smc(self, mr: float) -> float:
        """Inverse material ratio: height at given material ratio %."""
        return float(np.interp(mr, self.material_ratio, self.height))

    def Smr(self, c: float) -> float:
        """Material ratio at given height."""
        # height is descending, so flip for np.interp (needs ascending x)
        return float(np.interp(c, self.height[::-1], self.material_ratio[::-1]))

    # --- Equivalent line (ISO 13565-2) ---

    def _compute_equivalent_line(self) -> tuple[float, float]:
        if self._eq_slope is not None and self._eq_intercept is not None:
            return self._eq_slope, self._eq_intercept

        mr = self.material_ratio
        h = self.height

        best_slope = -np.inf
        best_start_idx = 0
        best_end_idx = 0

        # Step 1: find the 40% window with minimum secant slope
        for i in range(len(mr)):
            if mr[i] > 60.0:
                break
            mr_end = mr[i] + 40.0
            h_end = self.Smc(mr_end)
            slope = (h_end - h[i]) / 40.0
            if slope > best_slope:
                best_slope = slope
                best_start_idx = i
                best_end_idx = _argclosest(mr, mr_end)

        # Step 2: fit a regression line through the curve within that window
        mr_window = mr[best_start_idx : best_end_idx + 1]
        h_window = h[best_start_idx : best_end_idx + 1]
        slope, intercept = np.polyfit(mr_window, h_window, 1)

        self._eq_slope = float(slope)
        self._eq_intercept = float(intercept)
        return self._eq_slope, self._eq_intercept

    # --- Sk parameters ---

    @property
    def Sk(self) -> float:
        """Core roughness depth (ISO 13565-2)."""
        slope, intercept = self._compute_equivalent_line()
        y_upper = intercept  # height at mr=0%
        y_lower = slope * 100.0 + intercept  # height at mr=100%
        return float(y_upper - y_lower)

    @property
    def Spk(self) -> float:
        """Reduced peak height (ISO 13565-2)."""
        _slope, intercept = self._compute_equivalent_line()
        y_upper = intercept
        smr1 = self.Smr(y_upper)
        if smr1 <= 0:
            return 0.0

        idx_upper = _argclosest(self.height, y_upper)
        # Area A1: integrate material_ratio from top to y_upper
        area = np.abs(
            np.trapezoid(
                self.material_ratio[: idx_upper + 1], x=self.height[: idx_upper + 1]
            )
        )
        return float(2.0 * area / smr1)

    @property
    def Svk(self) -> float:
        """Reduced valley depth (ISO 13565-2)."""
        slope, intercept = self._compute_equivalent_line()
        y_lower = slope * 100.0 + intercept
        smr2 = self.Smr(y_lower)
        base = 100.0 - smr2
        if base <= 0:
            return 0.0

        idx_lower = _argclosest(self.height, y_lower)
        # Area A2: integrate (100 - material_ratio) from y_lower to bottom
        area = np.abs(
            np.trapezoid(
                100.0 - self.material_ratio[idx_lower:], x=self.height[idx_lower:]
            )
        )
        return float(2.0 * area / base)

    @property
    def Smr1(self) -> float:
        """Peak material ratio % (ISO 13565-2)."""
        _, intercept = self._compute_equivalent_line()
        return float(self.Smr(intercept))

    @property
    def Smr2(self) -> float:
        """Valley material ratio % (ISO 13565-2)."""
        slope, intercept = self._compute_equivalent_line()
        y_lower = slope * 100.0 + intercept
        return float(self.Smr(y_lower))

    # --- Volume parameters (ISO 25178-2) ---

    def _Vm(self, mr: float) -> float:
        """Material volume above Smc(mr)."""
        idx = _argclosest(self.height, self.Smc(mr))
        return float(
            np.abs(
                np.trapezoid(self.material_ratio[: idx + 1], x=self.height[: idx + 1])
            )
            / 100.0
        )

    def _Vv(self, mr: float) -> float:
        """Void volume below Smc(mr)."""
        idx = _argclosest(self.height, self.Smc(mr))
        return float(
            np.abs(np.trapezoid(100.0 - self.material_ratio[idx:], x=self.height[idx:]))
            / 100.0
        )

    @property
    def Vmp(self) -> float:
        """Peak material volume at p=10% (mm³/mm²)."""
        return self._Vm(10.0)

    @property
    def Vmc(self) -> float:
        """Core material volume between p=10% and q=80% (mm³/mm²)."""
        return self._Vm(80.0) - self._Vm(10.0)

    @property
    def Vvc(self) -> float:
        """Core void volume between p=10% and q=80% (mm³/mm²)."""
        return self._Vv(10.0) - self._Vv(80.0)

    @property
    def Vvv(self) -> float:
        """Pit void volume at q=80% (mm³/mm²)."""
        return self._Vv(80.0)
