from __future__ import annotations

from typing import TYPE_CHECKING, Any

import matplotlib.pyplot as plt
import numpy as np

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


def plot_surface_3d(
    surface: Surface,
    ax: Axes3D | None = None,
    cmap: str = "viridis",
    max_points: int = 300,
    colorbar: bool = True,
    **kwargs: Any,
) -> Axes3D:
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")  # type: ignore[assignment]

    ny, nx = surface.shape
    step_x = max(1, nx // max_points)
    step_y = max(1, ny // max_points)

    X, Y = np.meshgrid(surface.x[::step_x], surface.y[::step_y])
    Z = surface.z[::step_y, ::step_x]

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
    **kwargs: Any,
) -> Figure:
    import plotly.graph_objects as go

    fig = go.Figure(
        data=go.Surface(
            x=surface.x,
            y=surface.y,
            z=surface.z,
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
