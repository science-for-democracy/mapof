import numpy as np

from mapof.core.objects.Experiment import Experiment


def extract_selected_distances(experiment: Experiment, election_ids: list[str]):
    n = len(election_ids)

    distances = np.zeros(shape=(n, n))
    for i in range(n):
        for j in range(i + 1, n):
            election_id_1 = election_ids[i]
            election_id_2 = election_ids[j]
            distances[i, j] = distances[j, i] = experiment.distances[election_id_1][
                election_id_2
            ]

    return distances


def extract_selected_coordinates(coordinates: list, election_ids: list[str]):
    return np.array([coordinates[election_id] for election_id in election_ids])


def extract_selected_coordinates_from_experiment(
    experiment: Experiment, election_ids: list[str]
):
    return extract_selected_coordinates(experiment.coordinates, election_ids)


def extract_calculated_distances(coordinates: np.array):
    n = coordinates.shape[0]
    calculated_distances = np.zeros(shape=(n, n))

    for i in range(n):
        pos_i = coordinates[i]
        for j in range(i + 1, n):
            pos_j = coordinates[j]
            calculated_distances[i, j] = calculated_distances[j, i] = np.linalg.norm(
                pos_i - pos_j
            )

    return calculated_distances
