"""EventLog — the forge run-record contract, the engine's third seam.

Scene -> Solver -> EventLog -> Result -> ChartSpec: a time-ordered record of
what happened during a run, mirroring the solver's internal event loop the way
Unreal Insights mirrors the frame loop. Animation, replay/what-if scrubbing,
and digital-twin comparison consume an EventLog; they never reach into solver
internals — and a real plant's observed events can be ingested as the SAME
type a simulation emits.

Named EventLog because forgecore.Trace is the ChartSpec series type.

Generic on purpose: `kind` is free-form for v1 (promote to a dialect once 2+
solvers emit logs); event-specific payload (job ids, states, dispositions)
rides in `attrs`. Emitting is optional — analytic solvers never will.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .spec import SPEC_VERSION


@dataclass
class Event:
    """One thing that happened at time t."""

    t: float
    kind: str
    subject: str = ""  # node id / job id / actor id
    attrs: dict[str, Any] = field(default_factory=dict)


@dataclass
class EventLog:
    """A run's time-ordered event record."""

    events: list[Event] = field(default_factory=list)
    meta: dict[str, Any] = field(default_factory=dict)  # seed, run_time, warmup_time, ...

    def add(self, t: float, kind: str, subject: str = "", **attrs: Any) -> None:
        """Append an event (emitter convenience)."""
        self.events.append(Event(t=t, kind=kind, subject=subject, attrs=attrs))

    def for_subject(self, subject: str) -> list[Event]:
        """Every event about one actor, in recorded order."""
        return [e for e in self.events if e.subject == subject]

    def to_dict(self) -> dict:
        d = asdict(self)
        d["spec_version"] = SPEC_VERSION
        return d
