#!/usr/bin/env python

from mapof.core.features.distortion import calculate_distortion, calculate_distortion_naive
from mapof.core.features.monotonicity import calculate_monotonicity, calculate_monotonicity_naive
from mapof.core.features.stability import calculate_stability


def get_main_local_feature(feature_id):
    return {}.get(feature_id)


def get_main_global_feature(feature_id):
    """ Return the function that calculates the feature with the given id. """
    return {
        'distortion': calculate_distortion,
        'distortion_naive': calculate_distortion_naive,
        'monotonicity': calculate_monotonicity,
        'monotonicity_naive': calculate_monotonicity_naive,
        'stability': calculate_stability,
            }.get(feature_id)
