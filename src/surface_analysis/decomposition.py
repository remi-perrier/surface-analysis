from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from surface_analysis.surface import Surface


@dataclass
class Decomposition:
    form: Surface
    waviness: Surface
    roughness: Surface
    micro_roughness: Surface | None
    lambda_c: float
    lambda_s: float | None
