registered_experiment_features = {}

features_embedding_related = {}


def register_experiment_feature(feature_id: str, is_embedding_related=False):

    def decorator(func):
        registered_experiment_features[feature_id] = func
        if is_embedding_related:
            features_embedding_related[feature_id] = func
        return func

    return decorator
