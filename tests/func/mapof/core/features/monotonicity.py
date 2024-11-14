from mapof.core.features.monotonicity import (
    calculate_monotonicity,
    calculate_monotonicity_naive,
)


class TestFeatures:

    def test_monotonicity_naive(self, mocker):
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

        monotonicity = calculate_monotonicity_naive(experiment, election_ids)

        assert len(monotonicity) == len(experiment.coordinates)

    def test_monotonicity(self, mocker):
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

        monotonicity = calculate_monotonicity(experiment, election_ids)
        monotonicity_naive = calculate_monotonicity_naive(experiment, election_ids)

        assert monotonicity == monotonicity_naive
