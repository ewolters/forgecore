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

from dataclasses import asdict, is_dataclass
from typing import Iterable, Protocol, runtime_checkable

from .spec import ChartSpec

SPINE = frozenset({"mean", "median", "std", "confidence", "title"})
CAPABILITY = frozenset({"usl", "lsl", "cp", "cpk", "sigma", "dpmo"})
FLOW = frozenset({"cycle_time", "arrival_rate", "service_rate", "servers", "utilization"})
BEHAVIOR = frozenset({"cooperation", "trust", "morale", "reciprocity", "withdrawal"})


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


_REGISTRY: dict[str, type] = {}

# Dialects checked, in order, by ResultMixin.dialect() dispatch.
_DIALECTS = (("capability", CAPABILITY), ("flow", FLOW), ("behavior", BEHAVIOR))


def result_registry() -> dict[str, type]:
    """Catalog of result types that inherit ResultMixin.

    Populated at import time via __init_subclass__, so completeness depends on
    the caller having imported the relevant solver packages — forgerender does
    not (and cannot) import its own consumers.
    """
    return dict(_REGISTRY)


class ResultMixin:
    """Opt-in base for solver result dataclasses.

    Satisfies the Result protocol's shape when the subclass also provides
    `summary` and `to_render` (left bespoke per result). Inheriting buys:
    auto-registration into the engine catalog, a default `to_dict`, and a
    single `dialect()` dispatch that validates the view with `speaks()`.
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _REGISTRY[cls.__name__] = cls

    def to_dict(self) -> dict:
        return asdict(self) if is_dataclass(self) else dict(vars(self))

    def dialect(self) -> dict:
        for name, vocab in _DIALECTS:
            view_fn = getattr(self, name, None)
            if callable(view_fn):
                view = view_fn()
                if not speaks(view, vocab):
                    raise ValueError(
                        f"{type(self).__name__}.{name}() speaks tokens outside {name}: "
                        f"{set(view) - vocab}"
                    )
                return view
        return {}
