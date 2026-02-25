from __future__ import annotations

import numpy as np
import pytest

from surface_analysis import Surface


class TestFromArray:
    def test_creates_float64(self):
        z = np.array([[1, 2], [3, 4]], dtype=np.int32)
        s = Surface.from_array(z, step_x=0.01, step_y=0.02)
        assert s.z.dtype == np.float64

    def test_stores_steps(self):
        s = Surface.from_array(np.zeros((3, 4)), step_x=0.1, step_y=0.2)
        assert s.step_x == 0.1
        assert s.step_y == 0.2


class TestGeometry:
    @pytest.fixture()
    def surface(self):
        return Surface.from_array(np.zeros((5, 10)), step_x=0.01, step_y=0.02)

    def test_size_x(self, surface):
        assert surface.size_x == pytest.approx(0.1)

    def test_size_y(self, surface):
        assert surface.size_y == pytest.approx(0.1)

    def test_x_coordinates(self, surface):
        x = surface.x
        assert len(x) == 10
        assert x[0] == pytest.approx(0.0)
        assert x[-1] == pytest.approx(0.09)

    def test_y_coordinates(self, surface):
        y = surface.y
        assert len(y) == 5
        assert y[0] == pytest.approx(0.0)
        assert y[-1] == pytest.approx(0.08)


class TestNaN:
    def test_no_nan(self):
        s = Surface.from_array(np.ones((3, 3)), step_x=0.01, step_y=0.01)
        assert s.nan_count == 0
        assert s.nan_ratio == pytest.approx(0.0)

    def test_with_nan(self):
        z = np.ones((4, 5))
        z[0, 0] = np.nan
        z[1, 2] = np.nan
        s = Surface.from_array(z, step_x=0.01, step_y=0.01)
        assert s.nan_count == 2
        assert s.nan_ratio == pytest.approx(2 / 20)


class TestISOParameters:
    def test_flat_surface_sa_sq_zero(self):
        s = Surface.from_array(np.full((10, 10), 5.0), step_x=0.01, step_y=0.01)
        assert s.Sa == pytest.approx(0.0)
        assert s.Sq == pytest.approx(0.0)

    def test_known_sa(self):
        # Half at +1, half at -1 → mean=0, Sa = mean(|z|) = 1.0
        z = np.ones((10, 10))
        z[:5, :] = -1.0
        s = Surface.from_array(z, step_x=0.01, step_y=0.01)
        assert s.Sa == pytest.approx(1.0)

    def test_known_sq(self):
        # Half at +1, half at -1 → Sq = sqrt(mean(z^2)) = 1.0
        z = np.ones((10, 10))
        z[:5, :] = -1.0
        s = Surface.from_array(z, step_x=0.01, step_y=0.01)
        assert s.Sq == pytest.approx(1.0)

    def test_sp_sv_sz(self):
        z = np.zeros((10, 10))
        z[0, 0] = 3.0
        z[1, 1] = -2.0
        s = Surface.from_array(z, step_x=0.01, step_y=0.01)
        mean = np.mean(z)
        assert s.Sp == pytest.approx(3.0 - mean)
        assert s.Sv == pytest.approx(mean - (-2.0))
        assert s.Sz == pytest.approx(5.0)

    def test_sz_equals_sp_plus_sv(self):
        z = np.random.default_rng(99).standard_normal((20, 20))
        s = Surface.from_array(z, step_x=0.01, step_y=0.01)
        assert s.Sz == pytest.approx(s.Sp + s.Sv)

    def test_ssk_zero_for_symmetric(self):
        # Symmetric distribution → Ssk = 0
        z = np.ones((10, 10))
        z[:5, :] = -1.0
        s = Surface.from_array(z, step_x=0.01, step_y=0.01)
        assert s.Ssk == pytest.approx(0.0, abs=1e-10)

    def test_sku_three_for_gaussian(self):
        # Large Gaussian sample → Sku ≈ 3
        rng = np.random.default_rng(42)
        z = rng.standard_normal((500, 500))
        s = Surface.from_array(z, step_x=0.01, step_y=0.01)
        assert s.Sku == pytest.approx(3.0, rel=0.05)

    def test_ssk_sku_zero_when_flat(self):
        s = Surface.from_array(np.full((10, 10), 42.0), step_x=0.01, step_y=0.01)
        assert s.Ssk == 0.0
        assert s.Sku == 0.0

    def test_parameters_with_nan(self):
        z = np.ones((10, 10))
        z[0, 0] = np.nan
        z[3, 7] = np.nan
        s = Surface.from_array(z, step_x=0.01, step_y=0.01)
        # All valid points are 1.0 → Sa=0, Sq=0
        assert s.Sa == pytest.approx(0.0)
        assert s.Sq == pytest.approx(0.0)
        assert s.Sp == pytest.approx(0.0)

    def test_sdq_tilted_plane(self):
        # z = x → dz/dx = 1, dz/dy = 0 → Sdq = 1
        nx, ny = 50, 50
        step = 0.01
        x = np.arange(nx) * step
        z = np.tile(x, (ny, 1))
        s = Surface.from_array(z, step_x=step, step_y=step)
        assert s.Sdq == pytest.approx(1.0, rel=0.05)

    def test_sdr_flat_is_zero(self):
        s = Surface.from_array(np.zeros((10, 10)), step_x=0.01, step_y=0.01)
        assert s.Sdr == pytest.approx(0.0, abs=1e-10)

    def test_parameters_keys(self):
        s = Surface.from_array(np.random.randn(10, 10), step_x=0.01, step_y=0.01)
        params = s.parameters()
        expected = {"Sa", "Sq", "Sp", "Sv", "Sz", "Ssk", "Sku", "Sdq", "Sdr"}
        assert set(params.keys()) == expected


class TestApply:
    def test_chains_transforms(self):
        from surface_analysis.transforms._base import Transformation

        class AddOne(Transformation):
            def transform(self, surface):
                return Surface(
                    z=surface.z + 1, step_x=surface.step_x, step_y=surface.step_y
                )

        s = Surface.from_array(np.zeros((3, 3)), step_x=0.01, step_y=0.01)
        result = s.apply(AddOne(), AddOne(), AddOne())
        assert result.z[0, 0] == pytest.approx(3.0)

    def test_empty_transforms(self):
        s = Surface.from_array(np.ones((3, 3)), step_x=0.01, step_y=0.01)
        result = s.apply()
        assert np.array_equal(result.z, s.z)
