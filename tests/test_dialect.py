"""Tests for the forge dialect vocabulary + Result protocol."""

from forgerender import CAPABILITY, SPINE, ChartSpec, Result


def test_spine_vocabulary():
    assert SPINE == frozenset({"mean", "median", "std", "confidence", "title"})


def test_capability_dialect_vocabulary():
    assert CAPABILITY == frozenset({"usl", "lsl", "cp", "cpk", "sigma", "dpmo"})


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
