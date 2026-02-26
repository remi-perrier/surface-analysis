from __future__ import annotations

import numpy as np
import pytest

from surface_analysis import Surface
from surface_analysis.decomposition import Decomposition


class TestDecompose:
    @pytest.fixture()
    def synthetic(self):
        from surface_analysis.io import generate_synthetic

        return generate_synthetic(nx=200, ny=200, seed=42)

    def test_returns_decomposition(self, synthetic):
        dec = synthetic.decompose(lambda_c=0.08, lambda_s=0.005)
        assert isinstance(dec, Decomposition)

    def test_all_layers_present(self, synthetic):
        dec = synthetic.decompose(lambda_c=0.08, lambda_s=0.005)
        assert isinstance(dec.form, Surface)
        assert isinstance(dec.waviness, Surface)
        assert isinstance(dec.roughness, Surface)
        assert isinstance(dec.micro_roughness, Surface)

    def test_without_lambda_s_micro_roughness_is_none(self, synthetic):
        dec = synthetic.decompose(lambda_c=0.08)
        assert dec.micro_roughness is None
        assert isinstance(dec.roughness, Surface)

    def test_reconstruction(self, synthetic):
        dec = synthetic.decompose(lambda_c=0.08, lambda_s=0.005)
        reconstructed = dec.form + dec.waviness + dec.roughness + dec.micro_roughness
        # Cascaded Gaussian filters introduce small numerical errors (~1e-6)
        np.testing.assert_allclose(reconstructed.z, synthetic.z, atol=1e-5, rtol=1e-4)

    def test_cutoffs_stored(self, synthetic):
        dec = synthetic.decompose(lambda_c=0.08, lambda_s=0.005)
        assert dec.lambda_c == pytest.approx(0.08)
        assert dec.lambda_s == pytest.approx(0.005)

    def test_cutoffs_stored_without_lambda_s(self, synthetic):
        dec = synthetic.decompose(lambda_c=0.08)
        assert dec.lambda_c == pytest.approx(0.08)
        assert dec.lambda_s is None

    def test_form_plane(self, synthetic):
        dec_plane = synthetic.decompose(form="plane", lambda_c=0.08)
        dec_poly = synthetic.decompose(form="polynomial", lambda_c=0.08)
        # Different degrees → different roughness
        assert dec_plane.roughness.Sa != pytest.approx(dec_poly.roughness.Sa, rel=0.01)

    def test_interpolation_nearest(self):
        z = np.ones((50, 50))
        z[10, 10] = np.nan
        s = Surface.from_array(z, step_x=0.001, step_y=0.001)
        dec = s.decompose(form="plane", lambda_c=0.01, interpolation="nearest")
        assert dec.roughness.nan_count == 0

    def test_handles_nan_surface(self):
        z = np.random.default_rng(42).standard_normal((50, 50))
        z[0, :5] = np.nan
        s = Surface.from_array(z, step_x=0.001, step_y=0.001)
        dec = s.decompose(form="plane", lambda_c=0.01)
        assert dec.roughness.nan_count == 0

    def test_unknown_form_raises(self, synthetic):
        with pytest.raises(ValueError, match="Unknown form"):
            synthetic.decompose(form="cylinder")

    def test_unknown_interpolation_raises(self, synthetic):
        with pytest.raises(ValueError, match="Unknown interpolation"):
            synthetic.decompose(interpolation="cubic")
