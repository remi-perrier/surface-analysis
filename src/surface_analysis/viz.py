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
    title: str | None = None,
    colorbar: bool = True,
    **kwargs: Any,
) -> Axes:
    if ax is None:
        _, ax = plt.subplots()

    extent = (0, surface.size_x, surface.size_y, 0)
    im = ax.imshow(surface.z, extent=extent, cmap=cmap, aspect="equal", **kwargs)

    ax.set_xlabel("x (mm)")
    ax.set_ylabel("y (mm)")

    if title is not None:
        ax.set_title(title)

    if colorbar:
        ax.figure.colorbar(im, ax=ax, label="z (mm)")

    return ax


def _subsample(
    surface: Surface,
    max_points: int,
) -> tuple[NDArray, NDArray, NDArray]:
    ny, nx = surface.shape
    total = nx * ny

    if total > max_points:
        ratio = np.sqrt(max_points / total)
        max_x = max(1, int(nx * ratio))
        max_y = max(1, int(ny * ratio))
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
    max_points: int = 90_000,
    equal_xy: bool = True,
    title: str | None = None,
    colorbar: bool = True,
    **kwargs: Any,
) -> Axes3D:
    if ax is None:
        fig = plt.figure(figsize=(14, 6))
        fig.subplots_adjust(left=0.02, right=0.85)
        ax = fig.add_subplot(111, projection="3d")  # type: ignore[assignment]

    X, Y, Z = _subsample(surface, max_points=max_points)
    surf = ax.plot_surface(X, Y, Z, cmap=cmap, **kwargs)

    if title is not None:
        ax.figure.suptitle(title)

    ax.set_xlabel("x (mm)", labelpad=10, fontsize=8)
    ax.set_ylabel("y (mm)", labelpad=10, fontsize=8)
    ax.set_zlabel("z (mm)", labelpad=10, fontsize=8)
    ax.zaxis.set_major_locator(plt.MaxNLocator(nbins=5))
    ax.tick_params(labelsize=7)

    if equal_xy:
        x_range = surface.size_x
        y_range = surface.size_y
        max_xy = max(x_range, y_range)
        min_xy = min(x_range, y_range)
        ax.set_box_aspect((x_range / max_xy, y_range / max_xy, min_xy / max_xy))

    if colorbar:
        ax.figure.colorbar(surf, ax=ax, shrink=0.5, pad=0.12, label="z (mm)")

    return ax


def plot_surface_3d_interactive(
    surface: Surface,
    cmap: str = "Viridis",
    max_points: int = 500_000,
    equal_xy: bool = True,
    title: str | None = None,
    **kwargs: Any,
) -> Figure:
    import plotly.graph_objects as go

    X, Y, Z = _subsample(surface, max_points=max_points)

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

    scene: dict[str, Any] = dict(
        xaxis_title="x (mm)",
        yaxis_title="y (mm)",
        zaxis_title="z (mm)",
    )
    if equal_xy:
        x_range = surface.size_x
        y_range = surface.size_y
        max_xy = max(x_range, y_range)
        min_xy = min(x_range, y_range)
        scene["aspectmode"] = "manual"
        scene["aspectratio"] = dict(
            x=x_range / max_xy,
            y=y_range / max_xy,
            z=min_xy / max_xy,
        )

    fig.update_layout(scene=scene, title=title)

    return fig
