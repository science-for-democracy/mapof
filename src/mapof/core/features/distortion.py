import numpy as np
from collections import defaultdict

from mapof.core.features.common import \
    extract_selected_coordinates_from_experiment, \
    extract_selected_distances, \
    extract_calculated_distances
from mapof.core.objects.Experiment import Experiment

from mapof.core.features.register import register_experiment_feature


@register_experiment_feature('distortion', is_embedding_related=True)
def calculate_distortion(
        experiment: Experiment,
        election_ids: list[str] = None,
        max_distance_percentage: float = 1.0,
        normalize: bool = True,
        diameter: tuple = ('ID', 'UN')
) -> dict:
    """ Calculates the distortion of the distances between the points in the experiment. """
    coordinates = extract_selected_coordinates_from_experiment(experiment, election_ids)

    desired_distances = extract_selected_distances(experiment, election_ids)
    calculated_distances = extract_calculated_distances(coordinates)

    original_diameter = experiment.distances[diameter[0]][diameter[1]]
    embedded_diameter = np.linalg.norm(np.array(experiment.coordinates[diameter[0]])
                                       - np.array(experiment.coordinates[diameter[1]]), ord=2)

    if normalize:
        calculated_distances /= embedded_diameter
        desired_distances /= original_diameter

    max_distance = np.max(desired_distances)
    allowed_distance = max_distance * max_distance_percentage

    n = len(election_ids)

    # Use triu_indices to get indices for upper triangle of the distance matrix, excluding the diagonal
    i_indices, j_indices = np.triu_indices(n, k=1)

    # Filter distances that are within the allowed distance
    valid_pairs = desired_distances[i_indices, j_indices] <= allowed_distance

    # Extract valid i and j indices
    i_filtered = i_indices[valid_pairs]
    j_filtered = j_indices[valid_pairs]

    # Calculate distortions for valid pairs
    d1 = desired_distances[i_filtered, j_filtered]
    d2 = calculated_distances[i_filtered, j_filtered]
    distortions = np.where(d1 > d2, d1 / d2, d2 / d1)

    # Initialize distortion lists for each election index using defaultdict to handle missing keys
    distortion_lists = defaultdict(list)

    # Assign distortions to corresponding indices
    for i, j, distortion in zip(i_filtered, j_filtered, distortions):
        distortion_lists[i].append(distortion)
        distortion_lists[j].append(distortion)

    # Calculate mean distortion for each election
    mean_distortions = [np.mean(distortion_lists[i]) if distortion_lists[i] else 0 for i in
                        range(n)]

    return {
        election: mean_distortions[i] for i, election in enumerate(election_ids)
    }


@register_experiment_feature('distortion_naive', is_embedding_related=True)
def calculate_distortion_naive(
        experiment: Experiment,
        election_ids: list[str] = None,
        max_distance_percentage: float = 1.0,
        normalize: bool = True,
        diameter: tuple = ('ID', 'UN')
) -> dict:
    """ Calculates the distortion of the distances between the points in the experiment
     using a naive approach. """
    coordinates = extract_selected_coordinates_from_experiment(experiment, election_ids)

    desired_distances = extract_selected_distances(experiment, election_ids)
    calculated_distances = extract_calculated_distances(coordinates)

    original_diameter = experiment.distances[diameter[0]][diameter[1]]
    embedded_diameter = np.linalg.norm(np.array(experiment.coordinates[diameter[0]])
                                       - np.array(experiment.coordinates[diameter[1]]), ord=2)

    if normalize:
        calculated_distances /= embedded_diameter
        desired_distances /= original_diameter

    max_distance = np.max(desired_distances)
    allowed_distance = max_distance * max_distance_percentage

    distortions = defaultdict(list)

    n = len(election_ids)
    for i in range(n):
        for j in range(i + 1, n):
            d1 = desired_distances[i, j]
            if d1 <= allowed_distance:
                d2 = calculated_distances[i, j]
                if d1 > d2:
                    my_distortion = d1 / d2
                else:
                    my_distortion = d2 / d1

                distortions[i].append(my_distortion)
                distortions[j].append(my_distortion)

    return {
        election: np.mean(distortions[i]) for i, election in enumerate(election_ids)
    }
