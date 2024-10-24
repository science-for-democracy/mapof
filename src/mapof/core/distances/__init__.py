import copy
from time import time
import numpy as np

import mapof.core.persistence.experiment_exports as exports
from mapof.core.inner_distances import map_str_to_func

def extract_distance_id(distance_id: str) -> (callable, str):
    if '-' in distance_id:
        inner_distance, main_distance = distance_id.split('-')
        inner_distance = map_str_to_func(inner_distance)
    else:
        main_distance = distance_id
        inner_distance = None
    return inner_distance, main_distance


def run_single_process(
        exp,
        instances_ids: list,
        distances: dict,
        times: dict,
        matchings: dict
) -> None:
    """ Single process for computing distances """

    for instance_id_1, instance_id_2 in instances_ids:

        start_time = time()
        distance = exp.get_distance(copy.deepcopy(exp.instances[instance_id_1]),
                                copy.deepcopy(exp.instances[instance_id_2]),
                                distance_id=copy.deepcopy(exp.distance_id))
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
    """ Multiple processes for computing distances """

    for instance_id_1, instance_id_2 in instances_ids:
        start_time = time()
        distance = experiment.get_distance(copy.deepcopy(experiment.instances[instance_id_1]),
                                copy.deepcopy(experiment.instances[instance_id_2]),
                                distance_id=copy.deepcopy(experiment.distance_id))
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

