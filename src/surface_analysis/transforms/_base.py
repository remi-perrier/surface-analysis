from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from surface_analysis.surface import Surface


@runtime_checkable
class Transformation(Protocol):
    def transform(self, surface: Surface) -> Surface: ...
