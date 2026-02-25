from __future__ import annotations

from typing import TYPE_CHECKING, Any

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from mpl_toolkits.mplot3d.axes3d import Axes3D
    from plotly.graph_objects import Figure

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


def _subsample(
    surface: Surface, max_points: int | None = None, percentage: float | None = None
) -> tuple[NDArray, NDArray, NDArray]:
    ny, nx = surface.shape

    if percentage is not None:
        ratio = np.sqrt(percentage / 100.0)
        max_x = max(1, int(nx * ratio))
        max_y = max(1, int(ny * ratio))
    elif max_points is not None:
        max_x = max_y = max_points
    else:
        max_x, max_y = nx, ny

    step_x = max(1, nx // max_x)
    step_y = max(1, ny // max_y)

    X, Y = np.meshgrid(surface.x[::step_x], surface.y[::step_y])
    Z = surface.z[::step_y, ::step_x]
    return X, Y, Z


def plot_surface_3d(
    surface: Surface,
    ax: Axes3D | None = None,
    cmap: str = "viridis",
    max_points: int = 300,
    percentage: float | None = None,
    colorbar: bool = True,
    **kwargs: Any,
) -> Axes3D:
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")  # type: ignore[assignment]

    X, Y, Z = _subsample(surface, max_points=max_points, percentage=percentage)
    surf = ax.plot_surface(X, Y, Z, cmap=cmap, **kwargs)

    ax.set_xlabel("x (mm)")
    ax.set_ylabel("y (mm)")
    ax.set_zlabel("z (mm)")

    if colorbar:
        ax.figure.colorbar(surf, ax=ax, shrink=0.5, label="z (mm)")

    return ax


def plot_surface_3d_interactive(
    surface: Surface,
    cmap: str = "Viridis",
    max_points: int = 2000,
    percentage: float | None = None,
    **kwargs: Any,
) -> Figure:
    import plotly.graph_objects as go

    X, Y, Z = _subsample(surface, max_points=max_points, percentage=percentage)

    fig = go.Figure(
        data=go.Surface(
            x=X[0],
            y=Y[:, 0],
            z=Z,
            colorscale=cmap,
            colorbar=dict(title="z (mm)"),
            **kwargs,
        )
    )

    fig.update_layout(
        scene=dict(
            xaxis_title="x (mm)",
            yaxis_title="y (mm)",
            zaxis_title="z (mm)",
        ),
    )

    return fig
