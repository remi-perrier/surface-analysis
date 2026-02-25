from surface_analysis.transforms._base import Transformation
from surface_analysis.transforms.filtering import Gaussian
from surface_analysis.transforms.interpolation import Linear, Nearest
from surface_analysis.transforms.projection import Plane, Polynomial


class Transforms:
    class interpolation:
        Linear = Linear
        Nearest = Nearest

    class projection:
        Polynomial = Polynomial
        Plane = Plane

    class filtering:
        Gaussian = Gaussian


__all__ = ["Transformation", "Transforms"]
