import csv
from pathlib import Path

import pytest

from mapof.core.persistence import experiment_exports as exports


class DummyExperiment:
    def __init__(self):
        self.experiment_id = "exp_alpha"
        self.embedding_id = "embed1"
        self.distance_id = "distx"
        self.instances = ["inst_a", "inst_b"]
        self.coordinates = {
            "inst_a": (0.333333, -0.444444),
            "inst_b": (-1.234567, 2.345678),
        }


def read_csv(path: Path):
    with path.open() as handle:
        return list(csv.reader(handle, delimiter=";"))


def test_export_feature_to_file_embedding(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    experiment = DummyExperiment()
    feature_dict = {
        "foo": {"inst_a": 1, "inst_b": 2},
        "bar": {"inst_a": 3, "inst_b": 4},
    }

    exports.export_feature_to_file(experiment, "monotonicity_triplets", feature_dict)

    path = (
        tmp_path
        / "experiments"
        / experiment.experiment_id
        / "features"
        / f"monotonicity_triplets_{experiment.embedding_id}.csv"
    )
    assert path.exists()
    rows = read_csv(path)
    assert rows[0] == ["instance_id", "foo", "bar"]
    assert rows[1] == ["inst_a", "1", "3"]
    assert rows[2] == ["inst_b", "2", "4"]


def test_export_feature_to_file_custom_filename(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    experiment = DummyExperiment()
    feature_dict = {
        "f1": {"inst_a": 7},
    }
    exports.export_feature_to_file(
        experiment, "custom_metric", feature_dict, saveas="custom_out"
    )

    path = (
        tmp_path
        / "experiments"
        / experiment.experiment_id
        / "features"
        / "custom_out.csv"
    )
    assert path.exists()
    rows = read_csv(path)
    assert rows == [["instance_id", "f1"], ["inst_a", "7"]]


def test_export_normalized_feature_to_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    experiment = DummyExperiment()
    feature_dict = {
        "instance_id": {"inst_a": "inst_a", "inst_b": "inst_b"},
        "value": {"inst_a": 0.1, "inst_b": 0.2},
    }
    exports.export_normalized_feature_to_file(
        experiment, feature_dict, saveas="normalized"
    )

    path = (
        tmp_path
        / "experiments"
        / experiment.experiment_id
        / "features"
        / "normalized.csv"
    )
    rows = read_csv(path)
    assert rows[0] == ["instance_id", "instance_id", "value"]
    assert rows[1] == ["inst_a", "inst_a", "0.1"]
    assert rows[2] == ["inst_b", "inst_b", "0.2"]


@pytest.mark.parametrize(
    "dim,expected_header,expected_rows",
    [
        (
            1,
            ["instance_id", "x"],
            [["inst_a", "0.33333"], ["inst_b", "-1.23457"]],
        ),
        (
            2,
            ["instance_id", "x", "y"],
            [["inst_a", "0.33333", "-0.44444"], ["inst_b", "-1.23457", "2.34568"]],
        ),
        (
            3,
            ["instance_id", "x", "y", "z"],
            [
                ["inst_a", "0.33333", "-0.44444", "0.0"],
                ["inst_b", "-1.23457", "2.34568", "1.11111"],
            ],
        ),
    ],
)
def test_export_embedding_to_file(tmp_path, monkeypatch, dim, expected_header, expected_rows):
    monkeypatch.chdir(tmp_path)
    experiment = DummyExperiment()
    my_pos = [
        (0.0, 0.0, 0.0),
        (1.0, 1.0, 1.111112),
    ]

    exports.export_embedding_to_file(experiment, "emb", None, dim, my_pos)

    file_name = f"emb_{experiment.distance_id}_{dim}d.csv"
    path = (
        tmp_path
        / "experiments"
        / experiment.experiment_id
        / "coordinates"
        / file_name
    )
    rows = read_csv(path)
    assert rows[0] == expected_header
    assert rows[1:] == expected_rows


def test_export_distances_to_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    experiment = DummyExperiment()
    distances = {"inst_a": {"inst_b": 5}}
    times = {"inst_a": {"inst_b": 0.25}}
    exports.export_distances_to_file(
        experiment,
        "l1",
        distances,
        times,
        ids=[("inst_a", "inst_b")],
    )

    path = (
        tmp_path
        / "experiments"
        / experiment.experiment_id
        / "distances"
        / "l1.csv"
    )
    rows = read_csv(path)
    assert rows == [
        ["instance_id_1", "instance_id_2", "distance", "time"],
        ["inst_a", "inst_b", "5", "0.25"],
    ]


def test_export_distances_multiple_processes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    experiment = DummyExperiment()
    dist_dir = (
        tmp_path
        / "experiments"
        / experiment.experiment_id
        / "distances"
    )
    dist_dir.mkdir(parents=True, exist_ok=True)
    distances = {"inst_a": {"inst_b": 1.5}}
    times = {"inst_a": {"inst_b": 0.5}}
    exports.export_distances_multiple_processes(
        experiment,
        [("inst_a", "inst_b")],
        distances,
        times,
        process_id=3,
    )

    path = (
        tmp_path
        / "experiments"
        / experiment.experiment_id
        / "distances"
        / f"{experiment.distance_id}_p3.csv"
    )
    rows = read_csv(path)
    assert rows == [
        ["instance_id_1", "instance_id_2", "distance", "time"],
        ["inst_a", "inst_b", "1.5", "0.5"],
    ]
