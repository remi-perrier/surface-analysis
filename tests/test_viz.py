from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.axes import Axes

from surface_analysis import Surface


@pytest.fixture(autouse=True)
def _close_figures():
    yield
    plt.close("all")


def _make_surface(ny=10, nx=15, step=0.01):
    z = np.random.default_rng(42).random((ny, nx))
    return Surface.from_array(z, step_x=step, step_y=step)


def test_plot_returns_axes():
    s = _make_surface()
    ax = s.plot()
    assert isinstance(ax, Axes)


def test_plot_accepts_ax():
    s = _make_surface()
    fig, ax = plt.subplots()
    returned = s.plot(ax=ax)
    assert returned is ax


def test_plot_no_crash_with_nan():
    z = np.full((10, 10), np.nan)
    s = Surface.from_array(z, step_x=0.01, step_y=0.01)
    ax = s.plot()
    assert isinstance(ax, Axes)


# --- Title ---


def test_plot_title():
    s = _make_surface()
    ax = s.plot(title="Test title")
    assert ax.get_title() == "Test title"


def test_plot_3d_title():
    s = _make_surface()
    ax = s.plot_3d(title="3D title")
    assert ax.figure._suptitle.get_text() == "3D title"


def test_plot_3d_interactive_title():
    import plotly.graph_objects as go

    s = _make_surface()
    fig = s.plot_3d_interactive(title="Interactive title")
    assert isinstance(fig, go.Figure)
    assert fig.layout.title.text == "Interactive title"


# --- Subsampling ---


def test_subsample_preserves_aspect_ratio():
    """Non-square surface should not become square after subsampling."""
    from surface_analysis.viz import _subsample

    s = _make_surface(ny=100, nx=500)
    _, _, Z = _subsample(s, max_points=1000)
    z_ny, z_nx = Z.shape
    assert z_nx > z_ny, "Subsampled grid should preserve rectangular aspect ratio"


# --- 3D matplotlib ---


def test_plot_3d_returns_axes():
    s = _make_surface()
    ax = s.plot_3d()
    assert isinstance(ax, Axes)


def test_plot_3d_accepts_ax():
    s = _make_surface()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    returned = s.plot_3d(ax=ax)
    assert returned is ax


def test_plot_3d_no_crash_with_nan():
    z = np.full((10, 10), np.nan)
    s = Surface.from_array(z, step_x=0.01, step_y=0.01)
    ax = s.plot_3d()
    assert isinstance(ax, Axes)


# --- 3D plotly interactive ---


def test_plot_3d_interactive_returns_figure():
    import plotly.graph_objects as go

    s = _make_surface()
    fig = s.plot_3d_interactive()
    assert isinstance(fig, go.Figure)


def test_plot_3d_interactive_no_crash_with_nan():
    import plotly.graph_objects as go

    z = np.full((10, 10), np.nan)
    s = Surface.from_array(z, step_x=0.01, step_y=0.01)
    fig = s.plot_3d_interactive()
    assert isinstance(fig, go.Figure)
