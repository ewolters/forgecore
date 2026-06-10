from forgecore import (
    Annotation, Axis, ChartSpec, Marker, ReferenceLine, Trace, Zone,
)


def test_chartspec_constructs_and_serializes():
    spec = ChartSpec(title="t", chart_type="control_chart")
    spec.add_trace([1, 2, 3], [4, 5, 6], name="Data")
    spec.add_reference_line(10.0, label="UCL")
    d = spec.to_dict()
    assert d["title"] == "t"
    assert d["chart_type"] == "control_chart"
    assert len(d["traces"]) == 1
    assert d["traces"][0]["name"] == "Data"
    assert d["reference_lines"][0]["value"] == 10.0


def test_to_dict_drops_none_interactive():
    assert "interactive" not in ChartSpec().to_dict()


def test_all_elements_importable():
    for cls in (Trace, ReferenceLine, Zone, Marker, Axis, Annotation, ChartSpec):
        assert cls is not None


def test_role_field_roundtrips():
    spec = ChartSpec()
    spec.add_trace([1], [2], role="data")
    spec.add_reference_line(10.0, role="control_limit")
    spec.add_zone(1.0, 2.0, role="sigma_zone")
    spec.add_marker([0], role="out_of_control")
    d = spec.to_dict()
    assert d["traces"][0]["role"] == "data"
    assert d["reference_lines"][0]["role"] == "control_limit"
    assert d["zones"][0]["role"] == "sigma_zone"
    assert d["markers"][0]["role"] == "out_of_control"


def test_role_defaults_empty():
    assert ChartSpec(traces=[Trace(x=[1], y=[2])]).to_dict()["traces"][0]["role"] == ""


def test_role_constants_match_spellings():
    from forgecore import (
        ROLE_CENTERLINE, ROLE_CONTROL_LIMIT, ROLE_DATA, ROLE_OUT_OF_CONTROL,
        ROLE_RUN_RULE, ROLE_SIGMA_ZONE, ROLE_SPEC_LIMIT,
    )
    assert ROLE_DATA == "data"
    assert ROLE_CENTERLINE == "centerline"
    assert ROLE_CONTROL_LIMIT == "control_limit"
    assert ROLE_OUT_OF_CONTROL == "out_of_control"
    assert ROLE_SPEC_LIMIT == "spec_limit"
    assert ROLE_RUN_RULE == "run_rule"
    assert ROLE_SIGMA_ZONE == "sigma_zone"


def test_roles_frozenset_is_complete():
    from forgecore import (
        ROLE_CENTERLINE, ROLE_CONTROL_LIMIT, ROLE_DATA, ROLE_OUT_OF_CONTROL,
        ROLE_RUN_RULE, ROLE_SIGMA_ZONE, ROLE_SPEC_LIMIT, ROLES,
    )
    assert ROLES == frozenset({
        ROLE_DATA, ROLE_CENTERLINE, ROLE_CONTROL_LIMIT, ROLE_OUT_OF_CONTROL,
        ROLE_SPEC_LIMIT, ROLE_RUN_RULE, ROLE_SIGMA_ZONE,
    })
