from __future__ import annotations

from typing import TYPE_CHECKING, Any

import matplotlib.pyplot as plt

if TYPE_CHECKING:
    from matplotlib.axes import Axes

    from surface_analysis.surface import Surface


def plot_surface(
    surface: Surface,
    ax: Axes | None = None,
    cmap: str = "viridis",
    colorbar: bool = True,
    **kwargs: Any,
) -> Axes:
    if ax is None:
        ax = plt.gca()

    extent = (0, surface.size_x, surface.size_y, 0)
    im = ax.imshow(surface.z, extent=extent, cmap=cmap, **kwargs)

    ax.set_xlabel("x (mm)")
    ax.set_ylabel("y (mm)")

    if colorbar:
        ax.figure.colorbar(im, ax=ax, label="z (mm)")

    return ax
