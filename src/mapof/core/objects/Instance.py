from abc import ABC


class Instance(ABC):
    """ Abstract instance object """

    def __init__(self,
                 experiment_id: str,
                 instance_id: str,
                 culture_id: str = None,
                 **kwargs):

        self.experiment_id = experiment_id
        self.instance_id = instance_id
        self.culture_id = culture_id
        self.features = {}
        self.printing_params = {}
        self.params = kwargs

        for key in ['color', 'alpha', 'marker', 'ms']:
            self.printing_params[key] = None
