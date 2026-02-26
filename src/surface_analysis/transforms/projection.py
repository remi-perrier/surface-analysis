from __future__ import annotations

from typing import Literal

import numpy as np

from surface_analysis.surface import Surface
from surface_analysis.transforms._base import Transformation


def _vandermonde(x: np.ndarray, y: np.ndarray, degree: int) -> np.ndarray:
    columns = []
    for i in range(degree + 1):
        for j in range(degree + 1 - i):
            columns.append(x**i * y**j)
    return np.column_stack(columns)


class Polynomial(Transformation):
    def __init__(
        self, degree: int = 2, mode: Literal["residual", "form"] = "residual"
    ) -> None:
        self.degree = degree
        self.mode = mode

    def transform(self, surface: Surface) -> Surface:
        z = surface.z
        ny, nx = z.shape

        x = np.arange(nx) * surface.step_x
        y = np.arange(ny) * surface.step_y
        X, Y = np.meshgrid(x, y)

        mask = np.isfinite(z)
        n_terms = (self.degree + 1) * (self.degree + 2) // 2
        n_valid = int(mask.sum())
        if n_valid < n_terms:
            raise ValueError(
                f"Cannot fit degree {self.degree} polynomial: "
                f"need at least {n_terms} valid points, got {n_valid}"
            )

        coeffs, _, _, _ = np.linalg.lstsq(
            _vandermonde(X[mask], Y[mask], self.degree), z[mask], rcond=None
        )
        form = (_vandermonde(X.ravel(), Y.ravel(), self.degree) @ coeffs).reshape(
            z.shape
        )

        z_out = form if self.mode == "form" else z - form
        return Surface(z=z_out, step_x=surface.step_x, step_y=surface.step_y)


class Plane(Transformation):
    def __init__(self, mode: Literal["residual", "form"] = "residual") -> None:
        self.mode = mode

    def transform(self, surface: Surface) -> Surface:
        return Polynomial(degree=1, mode=self.mode).transform(surface)
