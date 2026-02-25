from __future__ import annotations

import numpy as np
import pytest

from surface_analysis.io import generate_synthetic


class TestGenerateSynthetic:
    def test_shape_and_step(self):
        s = generate_synthetic(nx=100, ny=80, step=0.002)
        assert s.shape == (80, 100)
        assert s.step_x == pytest.approx(0.002)
        assert s.step_y == pytest.approx(0.002)

    def test_reproducible_with_seed(self):
        s1 = generate_synthetic(nx=50, ny=50, seed=123)
        s2 = generate_synthetic(nx=50, ny=50, seed=123)
        np.testing.assert_array_equal(s1.z, s2.z)

    def test_different_with_different_seed(self):
        s1 = generate_synthetic(nx=50, ny=50, seed=1)
        s2 = generate_synthetic(nx=50, ny=50, seed=2)
        assert not np.array_equal(s1.z, s2.z)

    def test_no_nan(self):
        s = generate_synthetic(nx=50, ny=50)
        assert s.nan_count == 0

    def test_has_form_component(self):
        # With large radius, form is small; with small radius, form dominates
        s_flat = generate_synthetic(
            nx=100,
            ny=100,
            radius=1e6,
            roughness_rms=0,
            noise_rms=0,
            waviness_amplitude=0,
        )
        s_curved = generate_synthetic(
            nx=100,
            ny=100,
            radius=1.0,
            roughness_rms=0,
            noise_rms=0,
            waviness_amplitude=0,
        )
        assert s_curved.Sz > s_flat.Sz * 10
