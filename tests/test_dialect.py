"""Tests for the forge dialect vocabulary + Result protocol."""

from dataclasses import dataclass

import pytest

from forgecore import (
    BEHAVIOR,
    CAPABILITY,
    FLOW,
    SPINE,
    ChartSpec,
    Result,
    ResultMixin,
    result_registry,
    speaks,
)


def test_spine_vocabulary():
    assert SPINE == frozenset({"mean", "median", "std", "confidence", "title"})


def test_capability_dialect_vocabulary():
    assert CAPABILITY == frozenset({"usl", "lsl", "cp", "cpk", "sigma", "dpmo"})


def test_flow_dialect_vocabulary():
    assert FLOW == frozenset(
        {"cycle_time", "arrival_rate", "service_rate", "servers", "utilization"}
    )


def test_behavior_dialect_vocabulary():
    assert BEHAVIOR == frozenset(
        {"cooperation", "trust", "morale", "reciprocity", "withdrawal"}
    )


def test_dialect_dispatch_returns_the_validated_behavior_view():
    class BehRes(ResultMixin):
        def behavior(self):
            return {"cooperation": 0.8, "morale": 0.7}

    assert BehRes().dialect() == {"cooperation": 0.8, "morale": 0.7}


def test_speaks_accepts_a_subset_view():
    # A result speaks the tokens it carries — subset, not the whole dialect.
    assert speaks({"utilization": 0.5, "cycle_time": 2.0}, FLOW)


def test_speaks_rejects_a_foreign_token():
    assert not speaks({"utilization": 0.5, "cpk": 1.0}, FLOW)


def test_speaks_accepts_a_full_view():
    assert speaks({k: 0 for k in CAPABILITY}, CAPABILITY)


def test_subclassing_result_mixin_auto_registers_the_type():
    class Widget(ResultMixin):
        pass

    assert result_registry().get("Widget") is Widget


def test_result_mixin_provides_to_dict_for_dataclass_subclass():
    @dataclass
    class Foo(ResultMixin):
        a: int = 1
        b: str = "x"

    assert Foo().to_dict() == {"a": 1, "b": "x"}


def test_dialect_dispatch_returns_the_validated_capability_view():
    class CapRes(ResultMixin):
        def capability(self):
            return {"cpk": 1.0, "sigma": 3.0}

    assert CapRes().dialect() == {"cpk": 1.0, "sigma": 3.0}


def test_dialect_dispatch_prefers_flow_when_only_flow_present():
    class FlowRes(ResultMixin):
        def flow(self):
            return {"cycle_time": 2.0, "utilization": 0.5}

    assert FlowRes().dialect() == {"cycle_time": 2.0, "utilization": 0.5}


def test_dialect_dispatch_raises_on_foreign_tokens():
    class Bad(ResultMixin):
        def flow(self):
            return {"cycle_time": 1.0, "cpk": 9.9}  # cpk is not a FLOW token

    with pytest.raises(ValueError):
        Bad().dialect()


def test_result_mixin_subclass_with_render_and_summary_conforms_to_result():
    class Conf(ResultMixin):
        summary = "ok"

        def to_render(self) -> ChartSpec:
            return ChartSpec()

    assert isinstance(Conf(), Result)


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
