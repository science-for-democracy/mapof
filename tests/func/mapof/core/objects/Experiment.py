from abc import ABC

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


class TestExperiment():

    def test_experiment_creation(self):
       experiment = MockExperiment()
       assert experiment is not None, "Experiment should be created successfully"
