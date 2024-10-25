import itertools
import math
from copy import deepcopy

import numpy as np


def map_str_to_func(name: str) -> callable:
    """
    Maps a string to a function.

    Parameters
    ----------
        name : str
            Name of the distance.

    Returns
    -------
        callable

    """
    return {'l1': l1,
            'l2': l2,
            'chebyshev': chebyshev,
            'hellinger': hellinger,
            'emd': emd,
            'emdinf': emdinf,
            'discrete': discrete,
            'single_l1': single_l1,
            'hamming': hamming,
            }.get(name)


def l1(vector_1: np.ndarray, vector_2: np.ndarray) -> float:
    """
    Computes the L1 distance.

    Parameters
    ----------
        vector_1 : np.ndarray
            First vector.
        vector_2 : np.ndarray
            Second vector.
    Returns
    -------
        float
            L1 distance.
    """
    return np.linalg.norm(vector_1 - vector_2, ord=1)


def l2(vector_1: np.ndarray, vector_2: np.ndarray) -> float:
    """
    Computes the L2 distance.

    Parameters
    ----------
        vector_1 : np.ndarray
            First vector.
        vector_2 : np.ndarray
            Second vector.
    Returns
    -------
        float
            L2 distance.
    """
    return np.linalg.norm(vector_1 - vector_2, ord=2)


def chebyshev(vector_1: list, vector_2: list) -> float:
    """
    Computes the Chebyshev distance.

    Parameters
    ----------
        vector_1 : list
            First vector.
        vector_2 : list
            Second vector.
    Returns
    -------
        float
            Chebyshev distance.
    """
    return max([abs(vector_1[i] - vector_2[i]) for i in range(len(vector_1))])


def hellinger(vector_1: list, vector_2: list) -> float:
    """
    Computes the Hellinger distance.

    Parameters
    ----------
        vector_1 : list
            First vector.
        vector_2 : list
            Second vector.
    Returns
    -------
        float
            Hellinger distance.
    """
    h1 = np.average(vector_1)
    h2 = np.average(vector_2)
    product = sum([math.sqrt(vector_1[i] * vector_2[i])
                   for i in range(len(vector_1))])
    return math.sqrt(1 - (1 / math.sqrt(h1 * h2 * len(vector_1) * len(vector_1)))
                     * product)


def discrete(vector_1, vector_2) -> int:
    """
    Computes the discrete distance.

    Parameters
    ----------
        vector_1
            First vector.
        vector_2
            Second vector.
    Returns
    -------
        int
            Discrete distance.
    """
    for i in range(len(vector_1)):
        if vector_1[i] != vector_2[i]:
            return 1
    return 0


def emd(vector_1: list, vector_2: list) -> float:
    """
    Computes the EMD distance.

    Parameters
    ----------
        vector_1 : list
            First vector.
        vector_2 : list
            Second vector.
    Returns
    -------
        float
            EMD distance.
    """
    vector_1 = deepcopy(vector_1)
    dirt = 0.
    for i in range(len(vector_1) - 1):
        surplus = vector_1[i] - vector_2[i]
        dirt += abs(surplus)
        vector_1[i + 1] += surplus
    return dirt


def _stretch(vector, mult):
    return [x for _ in range(mult) for x in vector]


def emdinf(vector_1: list, vector_2: list) -> float:
    """
    Computes the EMD-infinity distance.

    Parameters
    ----------
        vector_1 : list
            First vector.
        vector_2 : list
            Second vector.
    Returns
    -------
        float
            EMD-infinity distance.
    """
    if len(vector_1) != len(vector_2):
        vector_1 = _stretch(vector_1, math.lcm(len(vector_1), len(vector_2)))
        vector_2 = _stretch(vector_2, math.lcm(len(vector_1), len(vector_2)))

    m = len(vector_1)
    cum_x = 0
    cum_y = 0
    res = 0
    for x, y in zip(vector_1, vector_2):
        cum_x_ = cum_x
        cum_y_ = cum_y
        cum_x += x
        cum_y += y

        if np.sign(cum_x_ - cum_y_) == np.sign(cum_x - cum_y):
            # Trapezoid case
            res += (abs(cum_x_ - cum_y_) + abs(cum_x - cum_y)) / m / 2
        else:
            # Two triangles case (works also for one triangle)
            d_1 = abs(cum_x_ - cum_y_)
            d_2 = abs(cum_x - cum_y)
            res += (d_1 * d_1 + d_2 * d_2) / (d_1 + d_2) / m / 2

    return res


def single_l1(value_1, value_2) -> float:
    """
    Computes the L1 distance between two values.

    Parameters
    ----------
        value_1
            First value.
        value_2
            Second values.
    Returns
    -------
        float
            L1 distance.
    """
    return abs(value_1 - value_2)


def hamming(set_1: set, set_2: set) -> int:
    """
    Computes the Hamming distance between two sets.

    Parameters
    ----------
        set_1 : set
            First vector.
        set_2 : set
            Second vector.
    Returns
    -------
        int
            Hamming distance.
    """
    return len(set_1.symmetric_difference(set_2))


def vote_to_pote(vote: list) -> list:
    """ Converts vote to pote (i.e. positional vote)

    Parameters
    ----------
        vote : list
            Ordinal vote.
    Returns
    -------
        list
            Potes (i.e. positional votes).
    """
    return [vote.index(i) for i in range(len(vote)+1) if i in vote]


def swap_distance(vote_1: list, vote_2: list, matching=None) -> int:
    """ Return: Swap distance between two votes """

    new_vote_2 = deepcopy(vote_2)
    if matching is not None:
        for i in range(len(vote_2)):
            new_vote_2[i] = matching[vote_2[i]]

    pote_1 = vote_to_pote(vote_1)
    pote_2 = vote_to_pote(new_vote_2)

    swap_distance = 0
    for i, j in itertools.combinations(pote_1, 2):
        if (pote_1[i] > pote_1[j] and pote_2[i] < pote_2[j]) or \
                (pote_1[i] < pote_1[j] and pote_2[i] > pote_2[j]):
            swap_distance += 1
    return swap_distance


def swap_distance_between_potes(pote_1: list, pote_2: list) -> int:
    """
    Computes the swap distance between two potes (i.e. positional votes).

    Parameters
    ----------
        pote_1 : list
            First vector.
        pote_2 : list
            Second vector.
    Returns
    -------
        int
            Swap distance.
    """
    swap_distance = 0
    for i, j in itertools.combinations(pote_1, 2):
        if (pote_1[i] > pote_1[j] and
            pote_2[i] < pote_2[j]) or \
                (pote_1[i] < pote_1[j] and
                 pote_2[i] > pote_2[j]):
            swap_distance += 1
    return swap_distance


def spearman_distance_between_potes(pote_1: list, pote_2: list) -> int:
    """
    Computes the Spearman distance between two potes (i.e. positional votes).

    Parameters
    ----------
        pote_1 : list
            First vector.
        pote_2 : list
            Second vector.
    Returns
    -------
        int
            Spearman distance.
    """
    return sum([abs(pote_1[c] - pote_2[c]) for c in range(len(pote_1))])
