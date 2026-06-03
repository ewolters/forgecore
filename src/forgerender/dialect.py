"""Forge dialect vocabulary + the Result protocol.

Solvers across the fleet emit ~80 different result dataclasses with no shared
base. Rather than rewrite them, the engine defines a thin vocabulary they speak
and a structural protocol they opt into.

  - SPINE: the tokens every result shares (mean/median/std/confidence/title).
  - CAPABILITY: the capability dialect (usl/lsl/cp/cpk/sigma/dpmo), spoken by
    forgespc + forgesim.

Defined here, in the zero-dep contract, so producers and consumers never drift
on spelling — the same single-source guarantee the ROLE_* constants provide.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from .spec import ChartSpec

SPINE = frozenset({"mean", "median", "std", "confidence", "title"})
CAPABILITY = frozenset({"usl", "lsl", "cp", "cpk", "sigma", "dpmo"})


@runtime_checkable
class Result(Protocol):
    """What the engine demands of any solver output."""

    summary: str

    def to_render(self) -> ChartSpec: ...
