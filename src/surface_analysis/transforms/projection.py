from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from ..surface import Surface


@dataclass
class PolynomialProjection:
    degree: int = 2

    def transform(self, surface: Surface) -> Surface:
        from ..surface import Surface

        z = surface.z
        ny, nx = z.shape

        # Build coordinate arrays
        x = np.arange(nx) * surface.step_x
        y = np.arange(ny) * surface.step_y
        X, Y = np.meshgrid(x, y)

        mask = np.isfinite(z)
        x_valid = X[mask]
        y_valid = Y[mask]
        z_valid = z[mask]

        # Build 2D Vandermonde matrix: 1, x, y, x^2, xy, y^2, ...
        columns = []
        for i in range(self.degree + 1):
            for j in range(self.degree + 1 - i):
                columns.append(x_valid**i * y_valid**j)
        A = np.column_stack(columns)

        # Least-squares fit
        coeffs, _, _, _ = np.linalg.lstsq(A, z_valid, rcond=None)

        # Reconstruct form on full grid
        columns_full = []
        for i in range(self.degree + 1):
            for j in range(self.degree + 1 - i):
                columns_full.append(X.ravel() ** i * Y.ravel() ** j)
        A_full = np.column_stack(columns_full)

        form = (A_full @ coeffs).reshape(z.shape)

        z_residual = z - form

        return Surface(z=z_residual, step_x=surface.step_x, step_y=surface.step_y)


@dataclass
class PlaneProjection:
    def transform(self, surface: Surface) -> Surface:
        return PolynomialProjection(degree=1).transform(surface)


def polynomial(degree: int = 2) -> PolynomialProjection:
    return PolynomialProjection(degree=degree)


def plane() -> PlaneProjection:
    return PlaneProjection()
