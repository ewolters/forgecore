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

from typing import Iterable, Protocol, runtime_checkable

from .spec import ChartSpec

SPINE = frozenset({"mean", "median", "std", "confidence", "title"})
CAPABILITY = frozenset({"usl", "lsl", "cp", "cpk", "sigma", "dpmo"})
FLOW = frozenset({"cycle_time", "arrival_rate", "service_rate", "servers", "utilization"})


def speaks(view: Iterable[str], dialect: frozenset[str]) -> bool:
    """True if a dialect-view carries only tokens the dialect defines.

    A result speaks the subset of tokens it actually carries; this guards
    against foreign or misspelled tokens, the same way the ROLE_* drift tests
    pin producers to a subset of ROLES.
    """
    return set(view) <= dialect


@runtime_checkable
class Result(Protocol):
    """What the engine demands of any solver output."""

    summary: str

    def to_render(self) -> ChartSpec: ...
