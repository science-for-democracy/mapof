from abc import ABC

import pytest

from mapof.core.objects.Experiment import Experiment

class MockExperiment(Experiment, ABC):

    def __init__(self, **kwargs):
        super().__init__()

    def get_distance(self, instance_id_1, instance_id_2, distance_id: str = None, **kwargs):
        pass

    def prepare_instances(self):
        pass

    def add_instance(self):
        pass

    def add_family(self):
        pass

    def add_instances_to_experiment(self):
        pass

    def add_folders_to_experiment(self):
        pass

    def import_controllers(self):
        pass

    def add_culture(self, name, function):
        pass

    def add_distance(self, name, function):
        pass

    def add_feature(self, name, function):
        pass


list_of_embedding_algorithms = {
    'fr',
    'kk',
    'mds',
}


class TestExperiment():

    def test_experiment_creation(self):
       experiment = MockExperiment()
       assert experiment is not None, "Experiment should be created successfully"

    @pytest.mark.parametrize("embedding_id", list_of_embedding_algorithms)
    def test_embedding(self, embedding_id):
        experiment = MockExperiment()

        experiment.distances = {'ID': {'UN': 1, 'a': 0.75, 'b': 0.5},
                                'UN': {'ID': 1, 'a': 0.25, 'b': 0.5},
                                'a': {'ID': 0.75, 'UN': 0.25, 'b': 0.13},
                                'b': {'ID': 0.5, 'UN': 0.5, 'a': 0.13}}

        experiment.is_exported = False

        experiment.embed_2d(embedding_id=embedding_id)

        assert len(experiment.coordinates) == len(experiment.distances)