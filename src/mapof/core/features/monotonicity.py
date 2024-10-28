
import numpy as np
from collections import defaultdict

from mapof.core.features.common import \
    extract_selected_distances, \
    extract_selected_coordinates_from_experiment
from mapof.core.objects.Experiment import Experiment

from mapof.core.features.register import register_experiment_feature


@register_experiment_feature('monotonicity', is_embedding_related=True)
def calculate_monotonicity(
        experiment: Experiment,
        election_ids: list[str] = None,
        max_distance_percentage: float = 1.0,
        error_tolerance: float = 0.
) -> dict:
    """ Calculate the monotonicity of the distances between the points in the experiment. """
    coordinates = extract_selected_coordinates_from_experiment(experiment, election_ids)
    desired_distances = extract_selected_distances(experiment, election_ids)
    calculated_distances = np.linalg.norm(coordinates[:, np.newaxis] - coordinates[np.newaxis, :], axis=2)

    max_distance = np.max(desired_distances)
    allowed_distance = max_distance * max_distance_percentage
    error_tolerance_squared = error_tolerance ** 2

    n = desired_distances.shape[0]

    # Create a mask for valid distances
    valid_mask = (desired_distances <= allowed_distance)

    # Create meshgrid for broadcasting
    i_idx, j_idx, k_idx = np.meshgrid(np.arange(n), np.arange(n), np.arange(n), indexing='ij')

    # Filter out diagonal elements and duplicates
    valid_triplets = (i_idx != j_idx) & (i_idx != k_idx) & (j_idx != k_idx) & valid_mask[i_idx, j_idx] & valid_mask[i_idx, k_idx]

    # Filtered indices
    i_filtered = i_idx[valid_triplets]
    j_filtered = j_idx[valid_triplets]
    k_filtered = k_idx[valid_triplets]

    # Calculate differences
    calc_diff = calculated_distances[i_filtered, j_filtered] - calculated_distances[i_filtered, k_filtered]
    des_diff = desired_distances[i_filtered, j_filtered] - desired_distances[i_filtered, k_filtered]

    # Condition checks
    is_good = (calc_diff * des_diff > 0) | (np.abs(calc_diff) <= error_tolerance * np.minimum(calculated_distances[i_filtered, j_filtered], calculated_distances[i_filtered, k_filtered]))

    # Use bincount for counting good and all distances
    good_counts = np.bincount(i_filtered, weights=is_good.astype(int), minlength=n)
    all_counts = np.bincount(i_filtered, minlength=n)

    # Calculate monotonicity
    monotonicity = np.zeros(n)
    non_zero_mask = all_counts > 0
    monotonicity[non_zero_mask] = good_counts[non_zero_mask] / all_counts[non_zero_mask]

    return {
        election: monotonicity[i] for i, election in enumerate(election_ids)
    }


@register_experiment_feature('monotonicity_naive', is_embedding_related=True)
def calculate_monotonicity_naive(
        experiment: Experiment,
        election_ids: list[str] = None,
        max_distance_percentage: float = 1.0,
        error_tolerance: float = 0.
) -> dict:
    """ Calculate the monotonicity of the distances between the points in the experiment
    using a naive approach."""
    coordinates = extract_selected_coordinates_from_experiment(experiment, election_ids)

    desired_distances = extract_selected_distances(experiment, election_ids)
    calculated_distances = np.linalg.norm(coordinates[:, np.newaxis] - coordinates[np.newaxis, :], axis=2)

    max_distance = np.max(desired_distances)

    allowed_distance = max_distance * max_distance_percentage

    n = desired_distances.shape[0]

    good_distances = defaultdict(int)
    all_distances = defaultdict(int)

    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            for k in range(n):
                if k == i or k == j:
                    continue

                if desired_distances[i, j] <= allowed_distance and desired_distances[i, k] <= allowed_distance:
                    calc = calculated_distances[i, j] - calculated_distances[i, k]
                    des = desired_distances[i, j] - desired_distances[i, k]

                    is_good = (calc * des > 0) or (abs(calc) <= error_tolerance *
                                                   min(calculated_distances[i, j], calculated_distances[i, k]))

                    all_distances[i] += 1
                    if is_good:
                        good_distances[i] += 1
    return {
        election: good_distances[i] / all_distances[i] for i, election in enumerate(election_ids)
    }
