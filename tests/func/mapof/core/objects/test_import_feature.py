from types import SimpleNamespace

import pytest

from mapof.core.objects.Experiment import Experiment


@pytest.fixture
def experiment_with_feature_csv(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    features_dir = tmp_path / "experiments" / "exp" / "features"
    features_dir.mkdir(parents=True)
    (features_dir / "my_feature.csv").write_text(
        "instance_id;value;time\n" "a;0.25;0.1\n" "b;None;0.1\n"
    )
    return SimpleNamespace(experiment_id="exp")


def test_import_feature_reads_values_from_experiment_folder(
    experiment_with_feature_csv,
):
    values = Experiment.import_feature(experiment_with_feature_csv, "my_feature")

    assert values == {"a": 0.25, "b": None}
