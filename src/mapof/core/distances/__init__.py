import copy
from time import time

import numpy as np

import mapof.core.persistence.experiment_exports as exports
from mapof.core.distances.inner_distances import (
    map_str_to_func,
    l1,
    l2,
    chebyshev,
    hellinger,
    emd,
    emdinf,
    discrete,
    single_l1,
    hamming,

    vote_to_pote,
    swap_distance,
    swap_distance_between_potes,
    spearman_distance_between_potes,
)

__all__ = [
    'run_single_process',
    'run_multiple_processes',
    'extract_distance_id',
    'map_str_to_func',
    'l1',
    'l2',
    'chebyshev',
    'hellinger',
    'emd',
    'emdinf',
    'discrete',
    'single_l1',
    'hamming',

    'vote_to_pote',
    'swap_distance',
    'swap_distance_between_potes',
    'spearman_distance_between_potes',
]


def extract_distance_id(distance_id: str) -> (callable, str):
    """
    Extracts inner distance and main distance from distance_id.

    Parameters
    ----------
        distance_id : str
            Name of the distance.

    Returns
    -------
        callable
            Inner distance.
        str
            Main distance.
    """
    if '-' in distance_id:
        inner_distance, main_distance = distance_id.split('-')
        inner_distance = map_str_to_func(inner_distance)
    else:
        main_distance = distance_id
        inner_distance = None
    return inner_distance, main_distance


def run_single_process(
        experiment,
        instances_ids: list,
        distances: dict,
        times: dict,
        matchings: dict
) -> None:
    """
    Calculates distances between each pair of instances (using single process).

    Parameters
    ----------
        experiment : Experiment
            Experiment object.
        instances_ids : list
            List of the Ids.
        distances :  dict
            Dictionary with distances between each pair of instances
        times : dict
            Dictionary with time of calculation of each distance.
        matchings : dict
            Dictionary with matchings between each pair of instances.

    Returns
    -------
        None
    """

    for instance_id_1, instance_id_2 in instances_ids:

        start_time = time()
        distance = experiment.get_distance(
            copy.deepcopy(experiment.instances[instance_id_1]),
            copy.deepcopy(experiment.instances[instance_id_2]),
            distance_id=copy.deepcopy(experiment.distance_id)
        )

        if type(distance) is tuple:
            distance, matching = distance
            matching = np.array(matching)
            matchings[instance_id_1][instance_id_2] = matching
            matchings[instance_id_2][instance_id_1] = np.argsort(matching)

        distances[instance_id_1][instance_id_2] = distance
        distances[instance_id_2][instance_id_1] = distances[instance_id_1][instance_id_2]
        times[instance_id_1][instance_id_2] = time() - start_time
        times[instance_id_2][instance_id_1] = times[instance_id_1][instance_id_2]


def run_multiple_processes(
        experiment,
        instances_ids: list,
        distances: dict,
        times: dict,
        matchings: dict,
        process_id: int
) -> None:
    """
    Calculates distances between each pair of instances (using multiple processes).

    Parameters
    ----------
        experiment : Experiment
            Experiment object.
        instances_ids : list
            List of the Ids.
        distances :  dict
            Dictionary with distances between each pair of instances
        times : dict
            Dictionary with time of calculation of each distance.
        matchings : dict
            Dictionary with matchings between each pair of instances.
        process_id : int
            ID of the process.

    Returns
    -------
        None
    """

    for instance_id_1, instance_id_2 in instances_ids:

        start_time = time()
        distance = experiment.get_distance(
            copy.deepcopy(experiment.instances[instance_id_1]),
            copy.deepcopy(experiment.instances[instance_id_2]),
            distance_id=copy.deepcopy(experiment.distance_id)
        )

        if type(distance) is tuple:
            distance, matching = distance
            matching = np.array(matching)
            matchings[instance_id_1][instance_id_2] = matching
            matchings[instance_id_2][instance_id_1] = np.argsort(matching)

        distances[instance_id_1][instance_id_2] = distance
        distances[instance_id_2][instance_id_1] = distances[instance_id_1][instance_id_2]
        times[instance_id_1][instance_id_2] = time() - start_time
        times[instance_id_2][instance_id_1] = times[instance_id_1][instance_id_2]

    if experiment.is_exported:
        exports.export_distances_multiple_processes(experiment,
                                                    instances_ids,
                                                    distances,
                                                    times,
                                                    process_id)
