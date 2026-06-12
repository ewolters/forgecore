"""Tests for EventLog — the run-record contract (the engine's third seam).

Named EventLog, not Trace: forgecore.Trace is the ChartSpec series type.
"""

from forgecore import Event, EventLog


def test_add_appends_an_event_with_attrs():
    log = EventLog()
    log.add(12.5, "start_process", "CNC", job=7)
    assert len(log.events) == 1
    e = log.events[0]
    assert (e.t, e.kind, e.subject) == (12.5, "start_process", "CNC")
    assert e.attrs == {"job": 7}


def test_for_subject_filters_one_actor_in_time_order():
    log = EventLog()
    log.add(1.0, "state_change", "CNC", state="processing")
    log.add(2.0, "arrival", "job-1")
    log.add(3.0, "state_change", "CNC", state="idle")
    states = [(e.t, e.attrs["state"]) for e in log.for_subject("CNC")]
    assert states == [(1.0, "processing"), (3.0, "idle")]


def test_to_dict_stamps_spec_version_and_serializes_events():
    log = EventLog(meta={"seed": 42, "run_time": 600.0})
    log.add(0.5, "arrival", "job-1")
    d = log.to_dict()
    assert d["spec_version"] == "1"
    assert d["meta"]["seed"] == 42
    assert d["events"][0] == {"t": 0.5, "kind": "arrival", "subject": "job-1", "attrs": {}}


def test_event_is_a_plain_record():
    e = Event(t=1.0, kind="complete", subject="job-9")
    assert e.attrs == {}
