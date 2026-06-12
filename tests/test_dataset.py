"""Tests for Dataset — the measurement input contract (Scene's twin)."""

from forgecore import Dataset, Series


def _ds():
    return Dataset(
        series=[
            Series(name="diameter", values=[5.1, 5.0, 5.2], unit="mm",
                   attrs={"subgroup": [1, 1, 2]}),
            Series(name="weight", values=[12.0, 12.1]),
        ],
        meta={"usl": 5.5, "lsl": 4.5},
    )


def test_get_returns_series_by_name():
    s = _ds().get("diameter")
    assert s is not None
    assert s.values == [5.1, 5.0, 5.2]
    assert s.unit == "mm"


def test_get_returns_none_for_unknown_name():
    assert _ds().get("nope") is None


def test_solver_tokens_ride_in_meta_and_attrs():
    ds = _ds()
    assert ds.meta["usl"] == 5.5
    assert ds.get("diameter").attrs["subgroup"] == [1, 1, 2]


def test_to_dict_stamps_spec_version():
    d = _ds().to_dict()
    assert d["spec_version"] == "1"
    assert d["series"][0]["name"] == "diameter"
    assert d["meta"] == {"usl": 5.5, "lsl": 4.5}
