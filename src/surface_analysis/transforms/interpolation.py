from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from scipy.interpolate import griddata

from surface_analysis.transforms._base import Transformation

if TYPE_CHECKING:
    from surface_analysis.surface import Surface


class Linear(Transformation):
    def transform(self, surface: Surface) -> Surface:
        from surface_analysis.surface import Surface

        z = surface.z
        if not np.any(np.isnan(z)):
            return surface

        mask = np.isfinite(z)
        ny, nx = z.shape
        yy, xx = np.mgrid[0:ny, 0:nx]

        points = np.column_stack([xx[mask], yy[mask]])
        values = z[mask]
        xi = np.column_stack([xx.ravel(), yy.ravel()])

        z_filled = griddata(points, values, xi, method="linear").reshape(z.shape)

        still_nan = np.isnan(z_filled)
        if still_nan.any():
            z_nearest = griddata(points, values, xi, method="nearest").reshape(z.shape)
            z_filled[still_nan] = z_nearest[still_nan]

        return Surface(z=z_filled, step_x=surface.step_x, step_y=surface.step_y)


class Nearest(Transformation):
    def transform(self, surface: Surface) -> Surface:
        from surface_analysis.surface import Surface

        z = surface.z
        if not np.any(np.isnan(z)):
            return surface

        mask = np.isfinite(z)
        ny, nx = z.shape
        yy, xx = np.mgrid[0:ny, 0:nx]

        points = np.column_stack([xx[mask], yy[mask]])
        values = z[mask]
        xi = np.column_stack([xx.ravel(), yy.ravel()])

        z_filled = griddata(points, values, xi, method="nearest").reshape(z.shape)

        return Surface(z=z_filled, step_x=surface.step_x, step_y=surface.step_y)
