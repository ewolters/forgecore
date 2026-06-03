"""Tests for the forge dialect vocabulary + Result protocol."""

from forgerender import CAPABILITY, FLOW, SPINE, ChartSpec, Result, speaks


def test_spine_vocabulary():
    assert SPINE == frozenset({"mean", "median", "std", "confidence", "title"})


def test_capability_dialect_vocabulary():
    assert CAPABILITY == frozenset({"usl", "lsl", "cp", "cpk", "sigma", "dpmo"})


def test_flow_dialect_vocabulary():
    assert FLOW == frozenset(
        {"cycle_time", "arrival_rate", "service_rate", "servers", "utilization"}
    )


def test_speaks_accepts_a_subset_view():
    # A result speaks the tokens it carries — subset, not the whole dialect.
    assert speaks({"utilization": 0.5, "cycle_time": 2.0}, FLOW)


def test_speaks_rejects_a_foreign_token():
    assert not speaks({"utilization": 0.5, "cpk": 1.0}, FLOW)


def test_speaks_accepts_a_full_view():
    assert speaks({k: 0 for k in CAPABILITY}, CAPABILITY)


def test_result_protocol_accepts_conforming_object():
    class Conforming:
        summary = "ok"

        def to_render(self) -> ChartSpec:
            return ChartSpec()

    assert isinstance(Conforming(), Result)


def test_result_protocol_rejects_object_missing_to_render():
    class NoRender:
        summary = "ok"

    assert not isinstance(NoRender(), Result)
