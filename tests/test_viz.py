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
