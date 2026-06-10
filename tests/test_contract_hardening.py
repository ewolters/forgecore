"""Contract hardening: collision-safe registry, spec_version, explicit dialect dispatch."""

import pytest

from forgerender import ChartSpec, ResultMixin, Scene
from forgerender.dialect import _REGISTRY


@pytest.fixture
def clean_probes():
    """Remove probe classes from the registry after each test."""
    yield
    for key in [k for k in _REGISTRY if "Probe" in k]:
        del _REGISTRY[key]


class TestRegistryCollision:
    def test_cross_module_name_collision_raises(self, clean_probes):
        type("CollisionProbe", (ResultMixin,), {"__module__": "pkg_one"})
        with pytest.raises(TypeError, match="CollisionProbe"):
            type("CollisionProbe", (ResultMixin,), {"__module__": "pkg_two"})

    def test_collision_keeps_first_registration(self, clean_probes):
        first = type("KeeperProbe", (ResultMixin,), {"__module__": "pkg_one"})
        with pytest.raises(TypeError):
            type("KeeperProbe", (ResultMixin,), {"__module__": "pkg_two"})
        assert _REGISTRY["KeeperProbe"] is first

    def test_same_module_redefinition_allowed(self, clean_probes):
        # Module reloads re-fire __init_subclass__ from the same module — not a collision.
        type("ReloadProbe", (ResultMixin,), {"__module__": "pkg_same"})
        latest = type("ReloadProbe", (ResultMixin,), {"__module__": "pkg_same"})
        assert _REGISTRY["ReloadProbe"] is latest


class TestSpecVersion:
    def test_chartspec_to_dict_carries_spec_version(self):
        from forgerender import SPEC_VERSION

        assert ChartSpec().to_dict()["spec_version"] == SPEC_VERSION

    def test_scene_to_dict_carries_spec_version(self):
        from forgerender import SPEC_VERSION

        assert Scene().to_dict()["spec_version"] == SPEC_VERSION


class _BilingualProbe(ResultMixin):
    """Speaks both capability and flow — first-match dispatch hides flow."""

    def capability(self):
        return {"cp": 1.2, "cpk": 1.1}

    def flow(self):
        return {"cycle_time": 4.0, "utilization": 0.8}


class TestExplicitDialect:
    def test_default_dispatch_returns_first_match(self):
        assert "cp" in _BilingualProbe().dialect()

    def test_explicit_name_reaches_shadowed_dialect(self):
        view = _BilingualProbe().dialect("flow")
        assert view == {"cycle_time": 4.0, "utilization": 0.8}

    def test_explicit_name_validates_with_speaks(self):
        class _ForeignProbe(ResultMixin):
            def flow(self):
                return {"cycle_time": 1.0, "not_a_flow_token": 2.0}

        with pytest.raises(ValueError, match="not_a_flow_token"):
            _ForeignProbe().dialect("flow")
        del _REGISTRY["_ForeignProbe"]

    def test_unknown_dialect_name_raises(self):
        with pytest.raises(ValueError, match="unknown dialect"):
            _BilingualProbe().dialect("nonsense")

    def test_explicit_name_without_view_returns_empty(self):
        class _MuteProbe(ResultMixin):
            pass

        assert _MuteProbe().dialect("flow") == {}
        del _REGISTRY["_MuteProbe"]
