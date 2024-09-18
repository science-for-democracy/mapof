import csv
import mapof.core.persistence.experiment_exports as persist


def test_something(mocker, tmp_path):
    exp = mocker.patch('mapof.core.objects.Experiment.Experiment', experiment_id="test_id")
    mocker.patch("os.getcwd", return_value=str(tmp_path))
    expected_dist = 143
    expected_time = 0.25
    distances = {
        "id1": {"id1": 0, "id2": expected_dist},
        "id2": {"id1": 2, "id2": 0}
    }
    times = {
        "id1": {"id1": 0, "id2": expected_time},
        "id2": {"id1": 0.12, "id2": 0}
    }
    dist_id = "test"
    persist.export_distances_to_file(
        exp,
        dist_id,
        distances,
        times,
        [("id1", "id2")])

    tested_file_path = tmp_path / "experiments" / exp.experiment_id / "distances" / (
            dist_id + ".csv")
    with open(tested_file_path, "r") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";")
        counter = 0
        for line in reader:
            counter += 1
            assert line['instance_id_1'] == 'id1'
            assert line['instance_id_2'] == 'id2'
            assert line['distance'] == str(expected_dist)
            assert line['time'] == str(expected_time)
        assert counter == 1
