import ast
import csv
import logging
import os

import numpy as np


def import_distances_from_file(
        experiment_id: str,
        distance_id: str,
        instance_ids: list
) -> dict:
    """
    Imports distances between each pair of instances from a file.

    Parameters
    ----------
        experiment_id : str
            Name of the experiment.
        distance_id : str
            Name of the distance.
        instance_ids : list
            List of the Ids.

    Returns
    -------
        dict
            Distances.
    """

    distances = {}

    file_name = f'{distance_id}.csv'
    path = os.path.join(os.getcwd(),
                        'experiments',
                        experiment_id,
                        'distances',
                        file_name)

    with open(path, 'r', newline='') as csv_file:

        reader = csv.DictReader(csv_file, delimiter=';')

        for row in reader:
            try:
                instance_id_1 = row['election_id_1']
                instance_id_2 = row['election_id_2']
            except:
                try:
                    instance_id_1 = row['instance_id_1']
                    instance_id_2 = row['instance_id_2']
                except:
                    pass
            if instance_id_1 not in instance_ids \
                    or instance_id_2 not in instance_ids:
                continue

            if instance_id_1 not in distances:
                distances[instance_id_1] = {}

            if instance_id_2 not in distances:
                distances[instance_id_2] = {}

            try:
                distances[instance_id_1][instance_id_2] = float(row['distance'])
                distances[instance_id_2][instance_id_1] = distances[instance_id_1][
                    instance_id_2]
            except KeyError:
                pass
    return distances


def add_distances_to_experiment(
        experiment_id: str,
        distance_id: str,
        instance_ids: list
) -> (dict, dict, dict, dict):
    """
    Imports precomputed distances between each pair of instances
    from a file while preparing an experiment.

    Parameters
    ----------
        experiment_id : str
            Name of the experiment.
        distance_id : str
            Name of the distance.
        instance_ids : list
            List of the Ids.


    Returns
    -------
        (dict, dict, dict, dict)
            distances, times, stds, mappings
    """

    try:
        file_name = f'{distance_id}.csv'
        path = os.path.join(os.getcwd(),
                            'experiments',
                            experiment_id,
                            'distances',
                            file_name)

        distances = {}
        times = {}
        stds = {}
        mappings = {}
        with open(path, 'r', newline='') as csv_file:

            reader = csv.DictReader(csv_file, delimiter=';')
            warn = False

            for row in reader:
                try:
                    instance_id_1 = row['election_id_1']
                    instance_id_2 = row['election_id_2']
                except:
                    try:
                        instance_id_1 = row['instance_id_1']
                        instance_id_2 = row['instance_id_2']
                    except:
                        pass

                if instance_id_1 not in instance_ids or \
                        instance_id_2 not in instance_ids:
                    continue

                if instance_id_1 not in distances:
                    distances[instance_id_1] = {}
                if instance_id_1 not in times:
                    times[instance_id_1] = {}
                if instance_id_1 not in stds:
                    stds[instance_id_1] = {}
                if instance_id_1 not in mappings:
                    mappings[instance_id_1] = {}

                if instance_id_2 not in distances:
                    distances[instance_id_2] = {}
                if instance_id_2 not in times:
                    times[instance_id_2] = {}
                if instance_id_2 not in stds:
                    stds[instance_id_2] = {}
                if instance_id_2 not in mappings:
                    mappings[instance_id_2] = {}

                try:
                    distances[instance_id_1][instance_id_2] = float(row['distance'])
                    distances[instance_id_2][instance_id_1] = distances[instance_id_1][
                        instance_id_2]
                except:
                    pass

                try:
                    times[instance_id_1][instance_id_2] = float(row['time'])
                    times[instance_id_2][instance_id_1] = times[instance_id_1][instance_id_2]
                except:
                    pass

                try:
                    stds[instance_id_1][instance_id_2] = float(row['std'])
                    stds[instance_id_2][instance_id_1] = stds[instance_id_1][instance_id_2]
                except:
                    pass

                try:
                    mappings[instance_id_1][instance_id_2] = ast.literal_eval(str(row['mapping']))
                    mappings[instance_id_2][instance_id_1] = np.argsort(
                        mappings[instance_id_1][instance_id_2])
                except:
                    pass

                if instance_id_1 not in instance_ids:
                    warn = True

            if warn:
                text = f'Possibly outdated distances are imported!'
                logging.warning(text)

        return distances, times, stds, mappings

    except FileNotFoundError:
        return dict(), dict(), dict(), dict()


def get_values_from_csv_file(
        experiment_id: str,
        feature_id: str,
        feature_long_id: str = None,
        upper_limit: float = np.infty,
        lower_limit: float = -np.infty,
        column_id: str = 'value'
) -> dict:
    """
    Imports values for a feature_id from a .csv file

    Parameters
    ----------
        experiment_id : str
            Name of the experiment.
        feature_id : str
            Name of the feature.
        feature_long_id: str
            Long name of the feature.
        upper_limit : float
            Upper limit for the values. If the value of a feature is greater than the upper limit,
            it is set to the upper limit.
        lower_limit : float
            Lower limit fot the values. If the value of a feature is smaller than the lower limit,
            it is set to the lower limit.
        column_id : str
            Name of the column to be imported.

    Returns
    -------
        dict
            Feature dictionary.
    """

    feature_long_id = feature_id if feature_long_id is None else feature_long_id

    path = os.path.join(os.getcwd(), "experiments", experiment_id, "features",
                        f'{feature_long_id}.csv')

    values = {}
    with open(path, 'r', newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';')

        for row in reader:
            election_id = row.get('instance_id', row.get('election_id'))
            value = row[column_id]

            if value is None or value in {'None', 'Blank', "''", '""', ''} or \
                    (column_id == 'time' and float(value) == 0.):
                values[election_id] = None
                continue

            value = float(value)
            values[election_id] = min(max(value, lower_limit), upper_limit)

    return values


def add_coordinates_to_experiment(
        experiment_id: str,
        distance_id: str,
        embedding_id: str,
        instance_ids: list,
        dim: int = 2,
        file_name: str = None
) -> dict:
    """
    Imports from a file precomputed coordinates of all the points,
    where each point refer to one instance

    Parameters
    ----------
        experiment_id : str
            Name of the experiment.
        distance_id : str
            Name of the distance.
        embedding_id : str
            Name of the embedding.
        instance_ids : list
            List of instance ids.
        dim : int
            Dimension.
        file_name : str
           Name of file in which the coordinates are stored.

    Returns
    -------
        dict
            Coordinates.
    """
    coordinates = {}
    if file_name is None:
        file_name = f'{embedding_id}_{distance_id}_{dim}d.csv'
    path = os.path.join(os.getcwd(), "experiments", experiment_id,
                        "coordinates", file_name)

    with open(path, 'r', newline='') as csv_file:

        reader = csv.DictReader(csv_file, delimiter=';')

        warn = False

        for row in reader:
            try:
                instance_id = row['instance_id']
            except KeyError:
                try:
                    instance_id = row['election_id']
                except KeyError:
                    pass

            if dim == 1:
                coordinates[instance_id] = [float(row['x'])]
            elif dim == 2:
                coordinates[instance_id] = [float(row['x']), float(row['y'])]
            elif dim == 3:
                coordinates[instance_id] = [float(row['x']), float(row['y']), float(row['z'])]

            if instance_id not in instance_ids:
                warn = True

        if warn:
            text = f'Possibly outdated coordinates are imported!'
            logging.warning(text)

    return coordinates
