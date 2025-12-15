import numpy as np
import pytest

from mapof.core import distances as distances_module


class DummyExperiment:
    def __init__(self, returns_matching=False, exported=False):
        self.instances = {"A": ["foo"], "B": ["bar"]}
        self.distance_id = "l1"
        self.experiment_id = "exp1"
        self.is_exported = exported
        self._returns_matching = returns_matching
        self.calls = 0

    def get_distance(self, instance_1, instance_2, distance_id):
        self.calls += 1
        if self._returns_matching:
            return 7, [1, 0]
        return 3


def patch_time(monkeypatch, values):
    iterator = iter(values)
    monkeypatch.setattr(distances_module, "time", lambda: next(iterator))


def patch_tqdm(monkeypatch):
    monkeypatch.setattr(distances_module, "tqdm", lambda iterable, **kwargs: iterable)


def test_extract_distance_id_with_inner():
    inner, main = distances_module.extract_distance_id("l1-emd")
    assert inner is distances_module.l1
    assert main == "emd"


def test_extract_distance_id_without_inner():
    inner, main = distances_module.extract_distance_id("emd")
    assert inner is None
    assert main == "emd"


def test_run_single_process_records_matchings(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    patch_tqdm(monkeypatch)
    patch_time(monkeypatch, [10.0, 10.5])
    experiment = DummyExperiment(returns_matching=True)
    ids = [("A", "B")]
    distances = {"A": {"B": None}, "B": {"A": None}}
    times = {"A": {"B": None}, "B": {"A": None}}
    matchings = {"A": {"B": None}, "B": {"A": None}}

    distances_module.run_single_process(experiment, ids, distances, times, matchings)

    assert distances["A"]["B"] == 7
    assert distances["B"]["A"] == 7
    assert np.array_equal(matchings["A"]["B"], np.array([1, 0]))
    assert np.array_equal(matchings["B"]["A"], np.array([1, 0]))
    assert times["A"]["B"] == pytest.approx(0.5)
    assert times["B"]["A"] == pytest.approx(0.5)
    assert experiment.calls == 1


def test_run_multiple_processes_exports_when_flagged(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    patch_tqdm(monkeypatch)
    patch_time(monkeypatch, [5.0, 5.3])
    experiment = DummyExperiment(exported=True)
    ids = [("A", "B")]
    distances = {"A": {"B": None}, "B": {"A": None}}
    times = {"A": {"B": None}, "B": {"A": None}}
    matchings = {"A": {"B": None}, "B": {"A": None}}

    called = {}

    def fake_export(exp, instances_ids, dist_arg, times_arg, process_id):
        called["exp"] = exp
        called["ids"] = instances_ids
        called["distances"] = dist_arg
        called["times"] = times_arg
        called["process_id"] = process_id

    monkeypatch.setattr(
        distances_module.exports,
        "export_distances_multiple_processes",
        fake_export,
    )

    distances_module.run_multiple_processes(
        experiment, ids, distances, times, matchings, process_id=2
    )

    assert distances["A"]["B"] == 3
    assert distances["B"]["A"] == 3
    assert times["A"]["B"] == pytest.approx(0.3)
    assert times["B"]["A"] == pytest.approx(0.3)
    assert called["exp"] is experiment
    assert called["ids"] == ids
    assert called["distances"] is distances
    assert called["times"] is times
    assert called["process_id"] == 2
