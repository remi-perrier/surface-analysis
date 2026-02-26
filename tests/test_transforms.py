from __future__ import annotations

import numpy as np
import pytest

from surface_analysis import Surface
from surface_analysis.transforms._base import Transformation
from surface_analysis.transforms.filtering import Gaussian
from surface_analysis.transforms.interpolation import Linear, Nearest
from surface_analysis.transforms.projection import Plane, Polynomial


class TestProtocol:
    @pytest.mark.parametrize("cls", [Linear, Nearest, Polynomial, Plane, Gaussian])
    def test_implements_transformation(self, cls):
        assert issubclass(cls, Transformation)


# --- Interpolation ---


class TestLinear:
    def test_no_nan_returns_same(self):
        s = Surface.from_array(np.ones((5, 5)), step_x=0.01, step_y=0.01)
        result = Linear().transform(s)
        assert result is s

    def test_fills_nan(self):
        z = np.ones((10, 10))
        z[5, 5] = np.nan
        s = Surface.from_array(z, step_x=0.01, step_y=0.01)
        result = Linear().transform(s)
        assert result.nan_count == 0
        assert result.z[5, 5] == pytest.approx(1.0, abs=0.1)

    def test_all_nan_raises(self):
        s = Surface(z=np.full((5, 5), np.nan), step_x=0.01, step_y=0.01)
        with pytest.raises(ValueError, match="no valid points"):
            Linear().transform(s)

    def test_edge_fallback_to_nearest(self):
        # NaN at corners outside convex hull of valid points → nearest fills them
        z = np.ones((10, 10))
        z[0, 0] = np.nan
        z[0, 9] = np.nan
        z[9, 0] = np.nan
        z[9, 9] = np.nan
        s = Surface.from_array(z, step_x=0.01, step_y=0.01)
        result = Linear().transform(s)
        assert result.nan_count == 0

    def test_does_not_mutate_input(self):
        z = np.ones((10, 10))
        z[5, 5] = np.nan
        s = Surface.from_array(z, step_x=0.01, step_y=0.01)
        z_before = s.z.copy()
        Linear().transform(s)
        np.testing.assert_array_equal(s.z, z_before)


class TestNearest:
    def test_no_nan_returns_same(self):
        s = Surface.from_array(np.ones((5, 5)), step_x=0.01, step_y=0.01)
        result = Nearest().transform(s)
        assert result is s

    def test_fills_nan(self):
        z = np.zeros((10, 10))
        z[5, 5] = np.nan
        z[5, 4] = 7.0
        s = Surface.from_array(z, step_x=0.01, step_y=0.01)
        result = Nearest().transform(s)
        assert result.nan_count == 0
        assert result.z[5, 5] == pytest.approx(7.0)

    def test_all_nan_raises(self):
        s = Surface(z=np.full((5, 5), np.nan), step_x=0.01, step_y=0.01)
        with pytest.raises(ValueError, match="no valid points"):
            Nearest().transform(s)


# --- Projection ---


class TestPolynomial:
    def test_removes_linear_tilt(self):
        nx, ny = 50, 50
        step = 0.01
        x = np.arange(nx) * step
        z = np.tile(x, (ny, 1))  # z = x → linear tilt
        s = Surface.from_array(z, step_x=step, step_y=step)

        result = Polynomial(degree=1).transform(s)
        assert result.Sq < 1e-10

    def test_removes_quadratic_form(self):
        nx, ny = 50, 50
        step = 0.01
        x = np.arange(nx) * step
        y = np.arange(ny) * step
        X, Y = np.meshgrid(x, y)
        z = 0.5 * X**2 + 0.3 * Y**2
        s = Surface.from_array(z, step_x=step, step_y=step)

        result = Polynomial(degree=2).transform(s)
        assert result.Sq < 1e-10

    def test_too_few_points_raises(self):
        z = np.full((10, 10), np.nan)
        z[0, 0] = 1.0
        s = Surface(z=z, step_x=0.01, step_y=0.01)
        with pytest.raises(ValueError, match="need at least"):
            Polynomial(degree=2).transform(s)

    def test_with_partial_nan(self):
        # Polynomial should fit only on valid points and still remove form
        nx, ny = 50, 50
        step = 0.01
        x = np.arange(nx) * step
        z = np.tile(x, (ny, 1))  # linear tilt
        z[0, :5] = np.nan
        z[-1, -5:] = np.nan
        s = Surface.from_array(z, step_x=step, step_y=step)

        result = Polynomial(degree=1).transform(s)
        valid = result.z[np.isfinite(result.z)]
        assert np.std(valid) < 1e-10

    def test_does_not_mutate_input(self):
        s = Surface.from_array(np.random.randn(20, 20), step_x=0.01, step_y=0.01)
        z_before = s.z.copy()
        Polynomial(degree=2).transform(s)
        np.testing.assert_array_equal(s.z, z_before)

    def test_preserves_steps(self):
        s = Surface.from_array(np.random.randn(20, 20), step_x=0.05, step_y=0.03)
        result = Polynomial(degree=2).transform(s)
        assert result.step_x == pytest.approx(0.05)
        assert result.step_y == pytest.approx(0.03)

    def test_mode_form_returns_fitted_polynomial(self):
        nx, ny = 50, 50
        step = 0.01
        x = np.arange(nx) * step
        y = np.arange(ny) * step
        X, Y = np.meshgrid(x, y)
        z = 0.5 * X**2 + 0.3 * Y**2
        s = Surface.from_array(z, step_x=step, step_y=step)

        form = Polynomial(degree=2, mode="form").transform(s)
        # Form should match the original (which is purely quadratic)
        np.testing.assert_allclose(form.z, z, atol=1e-10)

    def test_form_plus_residual_equals_original(self):
        rng = np.random.default_rng(42)
        z = rng.standard_normal((30, 30))
        s = Surface.from_array(z, step_x=0.01, step_y=0.01)

        residual = Polynomial(degree=2).transform(s)
        form = Polynomial(degree=2, mode="form").transform(s)
        reconstructed = form + residual
        np.testing.assert_allclose(reconstructed.z, s.z, atol=1e-10)


class TestPlane:
    def test_delegates_to_polynomial_degree_1(self):
        nx, ny = 30, 30
        step = 0.01
        x = np.arange(nx) * step
        y = np.arange(ny) * step
        X, Y = np.meshgrid(x, y)
        z = 2.0 * X + 3.0 * Y + 1.0
        s = Surface.from_array(z, step_x=step, step_y=step)

        result = Plane().transform(s)
        assert result.Sq < 1e-10


# --- Filtering ---


class TestGaussian:
    def test_cutoff_zero_raises(self):
        with pytest.raises(ValueError, match="positive"):
            Gaussian(cutoff=0)

    def test_cutoff_negative_raises(self):
        with pytest.raises(ValueError, match="positive"):
            Gaussian(cutoff=-1)

    def test_highpass_lowpass_reconstruct(self):
        z = np.random.default_rng(42).standard_normal((50, 50))
        s = Surface.from_array(z, step_x=0.01, step_y=0.01)
        cutoff = 0.1

        lowpass = Gaussian(cutoff=cutoff, mode="lowpass").transform(s)
        highpass = Gaussian(cutoff=cutoff, mode="highpass").transform(s)
        reconstructed = lowpass.z + highpass.z

        np.testing.assert_allclose(reconstructed, s.z, atol=1e-10)

    def test_highpass_removes_low_frequency(self):
        # Sine with wavelength >> cutoff should be removed by highpass
        nx, ny = 500, 100
        step = 0.001
        x = np.arange(nx) * step
        z = np.tile(np.sin(2 * np.pi * x / 0.4), (ny, 1))  # wavelength = 0.4 mm
        s = Surface.from_array(z, step_x=step, step_y=step)

        result = Gaussian(cutoff=0.05, mode="highpass").transform(s)
        assert result.Sq < s.Sq * 0.1

    def test_nan_preserved_at_edges(self):
        z = np.ones((20, 20))
        z[0, :] = np.nan
        s = Surface(z=z, step_x=0.01, step_y=0.01)

        result = Gaussian(cutoff=0.05, mode="lowpass").transform(s)
        assert result.nan_count == 0  # NaN-safe filter fills from neighbors

    def test_does_not_mutate_input(self):
        s = Surface.from_array(np.random.randn(20, 20), step_x=0.01, step_y=0.01)
        z_before = s.z.copy()
        Gaussian(cutoff=0.05).transform(s)
        np.testing.assert_array_equal(s.z, z_before)

    def test_preserves_steps(self):
        s = Surface.from_array(np.random.randn(20, 20), step_x=0.05, step_y=0.03)
        result = Gaussian(cutoff=0.1).transform(s)
        assert result.step_x == pytest.approx(0.05)
        assert result.step_y == pytest.approx(0.03)


# --- Composition ---


class TestComposition:
    def test_full_pipeline(self):
        from surface_analysis.io import generate_synthetic

        s = generate_synthetic(nx=100, ny=100, seed=42)
        result = s.apply(
            Linear(),
            Polynomial(degree=2),
            Gaussian(cutoff=0.008),
        )
        # Roughness should be much smaller than original (form removed)
        assert result.Sq < s.Sq
        assert result.nan_count == 0
