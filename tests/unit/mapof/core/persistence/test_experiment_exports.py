import os
import mapof.core.objects as objects
import mapof.core.persistence as persist

def test_something(mocker, tmp_path):
    mocker.patch.multiple(objects.Experiment, __abstractmethods__=set())
    experiment = objects.Experiment(experiment_id = "test_id")
    mocker.patch("os.getcwd", tmp_path)
    distances = {
     "id1": { "id1": 0, "id2": 1},
     "id2": { "id1": 2, "id2": 0}
     }
    times = {
     "id1": { "id1": 0.1, "id2": 0.25},
     "id2": { "id1": 0.2, "id2": 0.0}
     }
    persist.export_distance_to_file(experiment,
            "test_distance_id", distances, times, False, ["id1", "id2"] )
    assert 0 == 0

