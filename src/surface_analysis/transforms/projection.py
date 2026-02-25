from __future__ import annotations

import numpy as np

from surface_analysis.surface import Surface
from surface_analysis.transforms._base import Transformation


class Polynomial(Transformation):
    def __init__(self, degree: int = 2):
        self.degree = degree

    def transform(self, surface: Surface) -> Surface:
        z = surface.z
        ny, nx = z.shape

        x = np.arange(nx) * surface.step_x
        y = np.arange(ny) * surface.step_y
        X, Y = np.meshgrid(x, y)

        mask = np.isfinite(z)
        n_terms = sum(
            1 for i in range(self.degree + 1) for j in range(self.degree + 1 - i)
        )
        n_valid = int(mask.sum())
        if n_valid < n_terms:
            raise ValueError(
                f"Cannot fit degree {self.degree} polynomial: "
                f"need at least {n_terms} valid points, got {n_valid}"
            )

        x_valid = X[mask]
        y_valid = Y[mask]
        z_valid = z[mask]

        # 2D Vandermonde: 1, x, y, x^2, xy, y^2, ...
        columns = []
        for i in range(self.degree + 1):
            for j in range(self.degree + 1 - i):
                columns.append(x_valid**i * y_valid**j)
        A = np.column_stack(columns)

        coeffs, _, _, _ = np.linalg.lstsq(A, z_valid, rcond=None)

        columns_full = []
        for i in range(self.degree + 1):
            for j in range(self.degree + 1 - i):
                columns_full.append(X.ravel() ** i * Y.ravel() ** j)
        A_full = np.column_stack(columns_full)

        form = (A_full @ coeffs).reshape(z.shape)
        z_residual = z - form

        return Surface(z=z_residual, step_x=surface.step_x, step_y=surface.step_y)


class Plane(Transformation):
    def transform(self, surface: Surface) -> Surface:
        return Polynomial(degree=1).transform(surface)
