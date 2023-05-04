
class Instance:

    def __init__(self,
                 experiment_id: str,
                 instance_id: str,
                 culture_id: str = None,
                 alpha: float = None,
                 **kwargs):

        self.experiment_id = experiment_id
        self.instance_id = instance_id
        self.culture_id = culture_id
        self.alpha = alpha
        self.printing_params = {}

