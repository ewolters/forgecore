"""Dataset — the forge measurement-input contract, Scene's twin.

Scene standardizes input for graph-shaped solvers; Dataset does the same for
data-shaped ones (SPC, capability, statistics), replacing raw arrays + ad-hoc
kwargs. Generic on purpose: solver-specific tokens (usl/lsl/target, subgroup
ids, censoring flags, timestamps) ride in `meta`/`attrs`. Solvers adapt a
Dataset via a thin from_dataset() — never a rewrite.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Optional

from .spec import SPEC_VERSION


@dataclass
class Series:
    """One named sequence of measurements."""

    name: str
    values: list[float] = field(default_factory=list)
    unit: str = ""
    attrs: dict[str, Any] = field(default_factory=dict)


@dataclass
class Dataset:
    """Typed measurement input — the shared container data-shaped solvers read."""

    series: list[Series] = field(default_factory=list)
    meta: dict[str, Any] = field(default_factory=dict)

    def get(self, name: str) -> Optional[Series]:
        """Return the series with this name, or None."""
        for s in self.series:
            if s.name == name:
                return s
        return None

    def to_dict(self) -> dict:
        d = asdict(self)
        d["spec_version"] = SPEC_VERSION
        return d
