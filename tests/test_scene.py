"""Tests for the Scene seam — the typed input graph, symmetric to ChartSpec."""

from forgerender import Edge, Node, Scene


def test_node_defaults_have_no_position_and_empty_attrs():
    n = Node(id="s1")
    assert n.position is None
    assert n.attrs == {}
    assert n.kind == ""


def test_node_carries_position_and_solver_attrs():
    n = Node(id="weld", name="Weld", kind="station", position=(3.0, 1.0),
             attrs={"cycle_time": 90.0})
    assert n.position == (3.0, 1.0)
    assert n.attrs["cycle_time"] == 90.0


def test_edge_carries_transport_attrs():
    e = Edge(from_id="cut", to_id="weld", attrs={"frequency": 12, "distance": 4.5})
    assert e.from_id == "cut"
    assert e.attrs["distance"] == 4.5


def test_scene_to_dict_is_json_shaped():
    scene = Scene(
        nodes=[Node(id="cut", kind="station", position=(0.0, 0.0)),
               Node(id="weld", kind="station", position=(3.0, 0.0))],
        edges=[Edge(from_id="cut", to_id="weld", attrs={"frequency": 12, "distance": 3.0})],
        meta={"unit": "m"},
    )
    d = scene.to_dict()
    assert [n["id"] for n in d["nodes"]] == ["cut", "weld"]
    assert d["edges"][0]["to_id"] == "weld"
    assert d["meta"]["unit"] == "m"


def test_scene_node_lookup_by_id():
    scene = Scene(nodes=[Node(id="a"), Node(id="b")])
    assert scene.node("b").id == "b"
    assert scene.node("missing") is None
