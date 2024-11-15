from mapof.core.features.distortion import (
    calculate_distortion,
    calculate_distortion_naive,
)


class TestFeatures:

    def test_distortion_naive(self, mocker):
        experiment = mocker.patch("mapof.core.objects.Experiment.Experiment")

        experiment.distances = {
            "ID": {"UN": 1, "a": 0.5, "b": 0.5},
            "UN": {"ID": 1, "a": 0.5, "b": 0.5},
            "a": {"ID": 1, "UN": 0.5, "b": 0.5},
            "b": {"ID": 1, "UN": 0.5, "a": 0.5},
        }

        experiment.coordinates = {
            "ID": [0, 0],
            "UN": [1, 1],
            "a": [0.12321, 0.4215],
            "b": [0.124214, -0.1],
        }

        election_ids = list(experiment.coordinates.keys())

        distortion = calculate_distortion_naive(experiment, election_ids)

        assert len(distortion) == len(experiment.coordinates)

    def test_distortion(self, mocker):
        experiment = mocker.patch("mapof.core.objects.Experiment.Experiment")

        experiment.distances = {
            "ID": {"UN": 1, "a": 0.5, "b": 0.5},
            "UN": {"ID": 1, "a": 0.5, "b": 0.5},
            "a": {"ID": 1, "UN": 0.5, "b": 0.5},
            "b": {"ID": 1, "UN": 0.5, "a": 0.5},
        }

        experiment.coordinates = {
            "ID": [0, 0],
            "UN": [1, 1],
            "a": [0.12321, 0.4215],
            "b": [0.124214, -0.1],
        }

        election_ids = list(experiment.coordinates.keys())

        distortion = calculate_distortion(experiment, election_ids)
        distortion_naive = calculate_distortion_naive(experiment, election_ids)

        assert distortion == distortion_naive
