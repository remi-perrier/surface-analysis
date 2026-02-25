from surface_analysis.transforms._base import Transformation
from surface_analysis.transforms.filtering import Gaussian
from surface_analysis.transforms.interpolation import Linear, Nearest
from surface_analysis.transforms.projection import Plane, Polynomial


class Transforms:
    class Interpolation:
        Linear = Linear
        Nearest = Nearest

    class Projection:
        Polynomial = Polynomial
        Plane = Plane

    class Filtering:
        Gaussian = Gaussian


__all__ = ["Transformation", "Transforms"]
