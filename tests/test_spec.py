from forgerender import (
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
