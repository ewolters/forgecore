"""Scene — the forge input contract.

A typed, JSON-serializable graph that every solver layer reads from. The
symmetric counterpart to ChartSpec: ChartSpec standardizes solver *output*,
Scene standardizes solver *input* (replacing loose df/config/**kwargs).

Generic on purpose: a node's solver-specific parameters (cycle_time, mtbf,
service_rate, ...) and an edge's transport parameters (frequency, distance,
buffer_capacity) ride in `attrs`. Solvers pull the tokens they speak and adapt
a Scene into their own typed input via a thin from_scene() — never a rewrite.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Optional


@dataclass
class Node:
    """A point in the process graph (source / station / sink / ...)."""

    id: str
    name: str = ""
    kind: str = ""  # "source", "station", "sink", or domain-specific
    position: Optional[tuple[float, float]] = None  # (x, y); None until placed
    attrs: dict[str, Any] = field(default_factory=dict)


@dataclass
class Edge:
    """A directed connection. Transport params (frequency, distance,
    buffer_capacity) live in attrs."""

    from_id: str
    to_id: str
    attrs: dict[str, Any] = field(default_factory=dict)


@dataclass
class Scene:
    """A typed process graph — the shared input every layer reads."""

    nodes: list[Node] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)
    meta: dict[str, Any] = field(default_factory=dict)

    def node(self, node_id: str) -> Optional[Node]:
        """Return the node with this id, or None."""
        for n in self.nodes:
            if n.id == node_id:
                return n
        return None

    def to_dict(self) -> dict:
        return asdict(self)
