from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from surface_analysis.decomposition import Decomposition
    from surface_analysis.transforms._base import Transformation


@dataclass
class Surface:
    z: NDArray[np.float64]  # (ny, nx) height map in mm
    step_x: float  # pixel spacing in mm
    step_y: float  # pixel spacing in mm

    # --- Arithmetic operators ---

    def copy(self) -> Surface:
        return Surface(z=self.z.copy(), step_x=self.step_x, step_y=self.step_y)

    def _check_compatible(self, other: Surface) -> None:
        if self.shape != other.shape:
            raise ValueError(f"Incompatible shapes: {self.shape} vs {other.shape}")
        if self.step_x != other.step_x or self.step_y != other.step_y:
            raise ValueError(
                f"Incompatible steps: ({self.step_x}, {self.step_y}) "
                f"vs ({other.step_x}, {other.step_y})"
            )

    def __add__(self, other: Surface) -> Surface:
        self._check_compatible(other)
        return Surface(z=self.z + other.z, step_x=self.step_x, step_y=self.step_y)

    def __sub__(self, other: Surface) -> Surface:
        self._check_compatible(other)
        return Surface(z=self.z - other.z, step_x=self.step_x, step_y=self.step_y)

    def __mul__(self, scalar: float) -> Surface:
        return Surface(z=self.z * scalar, step_x=self.step_x, step_y=self.step_y)

    def __rmul__(self, scalar: float) -> Surface:
        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> Surface:
        return Surface(z=self.z / scalar, step_x=self.step_x, step_y=self.step_y)

    def __neg__(self) -> Surface:
        return Surface(z=-self.z, step_x=self.step_x, step_y=self.step_y)

    # --- Transforms ---

    def apply(self, *transforms: Transformation) -> Surface:
        result = self
        for t in transforms:
            result = t.transform(result)
        return result

    # --- Factory methods ---

    @classmethod
    def from_datx(cls, path: str) -> Surface:
        from surface_analysis.io import load_datx

        return load_datx(path)

    @classmethod
    def from_array(cls, z: NDArray, step_x: float, step_y: float) -> Surface:
        return cls(z=np.asarray(z, dtype=np.float64), step_x=step_x, step_y=step_y)

    # --- Geometry ---

    @property
    def shape(self) -> tuple[int, int]:
        return self.z.shape

    @property
    def n_points(self) -> int:
        return self.z.size

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

    # --- Decomposition ---

    def decompose(
        self,
        form: Literal["plane", "polynomial"] = "polynomial",
        lambda_c: float = 0.8,
        lambda_s: float | None = None,
        interpolation: Literal["linear", "nearest"] = "linear",
    ) -> Decomposition:
        """Decompose surface into form, waviness, roughness, and micro-roughness.

        Follows the ISO 25178-3 F/S/L pipeline: interpolation, form removal,
        then Gaussian filtering to separate spectral bands.

        Parameters
        ----------
        form : {"plane", "polynomial"}
            Form removal strategy. "plane" fits degree 1, "polynomial" degree 2.
        lambda_c : float
            Cutoff wavelength (mm) separating waviness from roughness.
        lambda_s : float or None
            Cutoff wavelength (mm) separating roughness from micro-roughness.
            If None, roughness includes all wavelengths below lambda_c.
        interpolation : {"linear", "nearest"}
            Method to fill NaN values before decomposition.

        Returns
        -------
        Decomposition
            Dataclass with form, waviness, roughness, micro_roughness surfaces.
        """
        from surface_analysis.decomposition import Decomposition
        from surface_analysis.transforms.filtering import Gaussian
        from surface_analysis.transforms.interpolation import Linear, Nearest
        from surface_analysis.transforms.projection import Polynomial

        # Resolve interpolation
        interp_map = {"linear": Linear, "nearest": Nearest}
        if interpolation not in interp_map:
            raise ValueError(
                f"Unknown interpolation {interpolation!r}, "
                f"expected one of {list(interp_map)}"
            )

        # Resolve form → polynomial degree
        form_map: dict[str, int] = {"plane": 1, "polynomial": 2}
        if form not in form_map:
            raise ValueError(f"Unknown form {form!r}, expected one of {list(form_map)}")
        degree = form_map[form]

        # Preprocessing — fill NaN
        filled = self.apply(interp_map[interpolation]())

        # F-operator — extract form, derive primary by subtraction
        form_surface = filled.apply(Polynomial(degree=degree, mode="form"))
        primary = filled - form_surface

        # Spectral decomposition — ISO 25178-3 F/S/L pipeline
        waviness = primary.apply(Gaussian(cutoff=lambda_c, mode="lowpass"))

        if lambda_s is not None:
            roughness = primary.apply(
                Gaussian(cutoff=lambda_s, mode="lowpass"),
                Gaussian(cutoff=lambda_c, mode="highpass"),
            )
            micro_roughness = primary.apply(Gaussian(cutoff=lambda_s, mode="highpass"))
        else:
            roughness = primary.apply(Gaussian(cutoff=lambda_c, mode="highpass"))
            micro_roughness = None

        return Decomposition(
            form=form_surface,
            waviness=waviness,
            roughness=roughness,
            micro_roughness=micro_roughness,
            lambda_c=lambda_c,
            lambda_s=lambda_s,
        )

    # --- Visualization ---

    def plot(self, title: str | None = None, **kwargs):
        from surface_analysis.viz import plot_surface

        return plot_surface(self, title=title, **kwargs)

    def plot_3d(
        self,
        max_points: int = 90_000,
        equal_xy: bool = True,
        title: str | None = None,
        **kwargs,
    ):
        from surface_analysis.viz import plot_surface_3d

        return plot_surface_3d(
            self,
            max_points=max_points,
            equal_xy=equal_xy,
            title=title,
            **kwargs,
        )

    def plot_3d_interactive(
        self,
        max_points: int = 500_000,
        equal_xy: bool = True,
        title: str | None = None,
        **kwargs,
    ):
        from surface_analysis.viz import plot_surface_3d_interactive

        return plot_surface_3d_interactive(
            self,
            max_points=max_points,
            equal_xy=equal_xy,
            title=title,
            **kwargs,
        )

    def __repr__(self) -> str:
        ny, nx = self.shape
        return (
            f"Surface({nx}x{ny}, "
            f"step=({self.step_x:.4f}, {self.step_y:.4f}) mm, "
            f"nan={self.nan_ratio:.1%})"
        )
