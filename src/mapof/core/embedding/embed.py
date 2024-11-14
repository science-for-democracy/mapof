import logging

import networkx as nx
import numpy as np

import mapof.core.persistence.experiment_exports as exports
import mapof.core.printing as pr
from mapof.core.embedding.kamada_kawai.kamada_kawai import KamadaKawai
from mapof.core.embedding.simulated_annealing.simulated_annealing import (
    SimulatedAnnealing,
)

try:
    from sklearn.manifold import MDS
    from sklearn.manifold import TSNE
    from sklearn.manifold import SpectralEmbedding
    from sklearn.manifold import LocallyLinearEmbedding
    from sklearn.manifold import Isomap
    from sklearn.decomposition import PCA
except ImportError as error:
    MDS = None
    TSNE = None
    SpectralEmbedding = None
    LocallyLinearEmbedding = None
    Isomap = None
    PCA = None
    print(error)


def embed(
    experiment,
    embedding_id: str = None,
    num_iterations: int = 1000,
    radius: float = np.inf,
    dim: int = 2,
    num_neighbors: int = None,
    method: str = None,
    zero_distance: float = 1.0,
    factor: float = 1.0,
    saveas: str = None,
    init_pos: dict = None,
    fixed: bool = True,
    attraction_factor: float = None,
    left=None,
    up=None,
    right=None,
    down=None,
    **kwargs,
) -> None:
    """Embeds the distances of an experiment using a given embedding method."""

    if attraction_factor is None:
        attraction_factor = 1
        if embedding_id in {"fr", "spring"}:
            attraction_factor = 2

    num_elections = len(experiment.distances)

    x = np.zeros((num_elections, num_elections))

    initial_positions = None

    if init_pos is not None:
        initial_positions = {}
        for i, instance_id_1 in enumerate(experiment.distances):
            if instance_id_1 in init_pos:
                initial_positions[i] = init_pos[instance_id_1]

    for i, instance_id_1 in enumerate(experiment.distances):
        for j, instance_id_2 in enumerate(experiment.distances):
            if i < j:

                experiment.distances[instance_id_1][instance_id_2] *= factor
                if embedding_id in {"fr", "spring"}:
                    if experiment.distances[instance_id_1][instance_id_2] == 0.0:
                        experiment.distances[instance_id_1][
                            instance_id_2
                        ] = zero_distance
                        experiment.distances[instance_id_2][
                            instance_id_1
                        ] = zero_distance
                    normal = True
                    if experiment.distances[instance_id_1][instance_id_2] > radius:
                        x[i][j] = 0.0
                        normal = False
                    if num_neighbors is not None:
                        tmp = experiment.distances[instance_id_1]
                        sorted_list_1 = list(
                            (dict(sorted(tmp.items(), key=lambda item: item[1]))).keys()
                        )
                        tmp = experiment.distances[instance_id_2]
                        sorted_list_2 = list(
                            (dict(sorted(tmp.items(), key=lambda item: item[1]))).keys()
                        )
                        if (instance_id_1 not in sorted_list_2[0:num_neighbors]) and (
                            instance_id_2 not in sorted_list_1[0:num_neighbors]
                        ):
                            x[i][j] = 0.0
                            normal = False
                    if normal:
                        x[i][j] = (
                            1.0 / experiment.distances[instance_id_1][instance_id_2]
                        )
                else:
                    x[i][j] = experiment.distances[instance_id_1][instance_id_2]
                x[i][j] = x[i][j] ** attraction_factor
                x[j][i] = x[i][j]

    dt = [("weight", float)]
    y = x.view(dt)
    graph = nx.from_numpy_array(y)

    if num_neighbors is None:
        num_neighbors = 100

    if embedding_id.lower() in {"fr", "spring"}:
        my_pos = nx.spring_layout(graph, iterations=num_iterations, dim=dim, **kwargs)
    elif embedding_id.lower() in {"mds"}:
        my_pos = MDS(
            n_components=dim,
            dissimilarity="precomputed",
            max_iter=num_iterations,
            normalized_stress="auto",
            **kwargs,
        ).fit_transform(x)
    elif embedding_id.lower() in {"tsne"}:
        my_pos = TSNE(n_components=dim, n_iter=num_iterations, **kwargs).fit_transform(
            x
        )
    elif embedding_id.lower() in {"se"}:
        my_pos = SpectralEmbedding(n_components=dim, **kwargs).fit_transform(x)
    elif embedding_id.lower() in {"isomap"}:
        my_pos = Isomap(
            n_components=dim, n_neighbors=num_neighbors, **kwargs
        ).fit_transform(x)
    elif embedding_id.lower() in {"lle"}:
        my_pos = LocallyLinearEmbedding(
            n_components=dim,
            n_neighbors=num_neighbors,
            max_iter=num_iterations,
            method=method,
        ).fit_transform(x)
    elif embedding_id.lower() in {"kk", "kamada-kawai", "kamada", "kawai"}:
        my_pos = KamadaKawai().embed(
            distances=x,
            initial_positions=initial_positions,
            fix_initial_positions=fixed,
        )
    elif embedding_id.lower() in {"simulated-annealing"}:
        my_pos = SimulatedAnnealing().embed(
            distances=x,
            initial_positions=initial_positions,
            fix_initial_positions=fixed,
        )
    elif embedding_id.lower() in {"geo"}:
        f1 = experiment.import_feature("voterlikeness_sqrt")
        f2 = experiment.import_feature("borda_diversity")
        for f in f1:
            if f1[f] is None:
                f1[f] = 0
            if f2[f] is None:
                f2[f] = 0
        my_pos = [[f1[e], f2[e]] for e in f1]
    elif embedding_id.lower() in {"pca"}:
        pca = PCA(n_components=2)
        principalComponents = pca.fit_transform(x)
        my_pos = principalComponents
    else:
        my_pos = []
        logging.warning("Unknown embedding method!")

    experiment.coordinates = {}
    for i, instance_id in enumerate(experiment.distances):
        experiment.coordinates[instance_id] = [my_pos[i][d] for d in range(dim)]

    pr.adjust_the_map(experiment, left=left, up=up, right=right, down=down)

    if experiment.is_exported:
        exports.export_embedding_to_file(experiment, embedding_id, saveas, dim, my_pos)
