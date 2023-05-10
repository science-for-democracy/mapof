#!/usr/bin/env python
import os

from mapel.elections.objects.ElectionExperiment import ElectionExperiment
import mapel.elections.cultures_ as cultures
import mapel.elections.features_ as features
import mapel.elections.distances_ as distances

try:
    from sklearn.manifold import MDS
    from sklearn.manifold import TSNE
    from sklearn.manifold import SpectralEmbedding
    from sklearn.manifold import LocallyLinearEmbedding
    from sklearn.manifold import Isomap
except ImportError as error:
    MDS = None
    TSNE = None
    SpectralEmbedding = None
    LocallyLinearEmbedding = None
    Isomap = None
    print(error)


class OrdinalElectionExperiment(ElectionExperiment):
    """Abstract set of elections."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_culture(self, name, function):
        cultures.add_ordinal_culture(name, function)

    def add_feature(self, name, function):
        features.add_ordinal_feature(name, function)

    def add_distance(self, name, function):
        distances.add_ordinal_distance(name, function)

    def add_folders_to_experiment(self) -> None:

        if not os.path.isdir("experiments/"):
            os.mkdir(os.path.join(os.getcwd(), "experiments"))

        if not os.path.isdir("images/"):
            os.mkdir(os.path.join(os.getcwd(), "images"))

        if not os.path.isdir("trash/"):
            os.mkdir(os.path.join(os.getcwd(), "trash"))

        try:
            os.mkdir(os.path.join(os.getcwd(), "experiments", self.experiment_id))

            list_of_folders = ['distances',
                               'features',
                               'coordinates',
                               'elections',
                               'matrices']

            for folder_name in list_of_folders:
                try:
                    os.mkdir(
                        os.path.join(os.getcwd(), "experiments", self.experiment_id, folder_name))
                except:
                    pass
        except:
            pass

        try:
            path = os.path.join(os.getcwd(), "experiments", self.experiment_id, "map.csv")

            with open(path, 'w') as file_csv:
                file_csv.write(
                    "size;num_candidates;num_voters;culture_id;params;color;alpha;family_id;label;marker;show\n")
                file_csv.write("3;10;100;ic;{};black;1;ic;Impartial Culture;o;t\n")
        except FileExistsError:
            print("Experiment already exists!")