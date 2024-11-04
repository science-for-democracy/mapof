import unittest
import numpy as np

from mapof.core.distances import *


class TestDistanceFunctions(unittest.TestCase):

    def test_map_str_to_func(self):
        self.assertEqual(map_str_to_func('l1'), l1)
        self.assertEqual(map_str_to_func('l2'), l2)
        self.assertEqual(map_str_to_func('chebyshev'), chebyshev)
        self.assertEqual(map_str_to_func('unknown'), None)

    def test_discrete(self):
        self.assertEqual(discrete([1, 2, 3], [1, 2, 3]), 0)
        self.assertEqual(discrete([1, 2, 3], [1, 2, 4]), 1)

    def test_single_l1(self):
        self.assertAlmostEqual(single_l1(3, 4), 1)
        self.assertAlmostEqual(single_l1(5.5, 2.5), 3)

    def test_l1(self):
        self.assertAlmostEqual(l1(np.array([1, 2, 3]), np.array([4, 5, 6])), 9)
        self.assertAlmostEqual(l1(np.array([1, 2, 3]), np.array([1, 2, 3])), 0)

    def test_l2(self):
        self.assertAlmostEqual(l2(np.array([1, 2, 3]), np.array([4, 5, 6])), 5.196152422706632)
        self.assertAlmostEqual(l2(np.array([1, 2, 3]), np.array([1, 2, 3])), 0)

    def test_chebyshev(self):
        self.assertEqual(chebyshev([1, 2, 3], [1, 2, 3]), 0)
        self.assertEqual(chebyshev([1, 2, 3], [3, 2, 1]), 2)

    def test_hellinger(self):
        self.assertAlmostEqual(hellinger([0.1, 0.9], [0.2, 0.8]), 0.10025221363557746)
        self.assertAlmostEqual(hellinger([1, 0], [1, 0]), 0)

    def test_emd(self):
        self.assertAlmostEqual(emd([1, 2, 3], [1, 2, 3]), 0)
        self.assertAlmostEqual(emd([1, 2, 3], [3, 2, 1]), 4)

    def test_emdinf(self):
        self.assertAlmostEqual(emdinf([1, 2, 3], [1, 2, 3]), 0)
        self.assertAlmostEqual(emdinf([1, 2, 3], [3, 2, 1]), 1.3333333333333333)

    def test_hamming(self):
        self.assertEqual(hamming({1, 2, 3}, {1, 2, 3}), 0)
        self.assertEqual(hamming({1, 2, 3}, {2, 3, 4}), 2)
        self.assertEqual(hamming({1, 2, 3}, {4, 5, 6}), 6)

    def test_vote_to_pote(self):
        self.assertEqual(vote_to_pote([1, 0, 2]), [1, 0, 2])
        self.assertEqual(vote_to_pote([0, 1, 2]), [0, 1, 2])

    def test_swap_distance(self):
        self.assertEqual(swap_distance([0, 1, 2], [0, 1, 2]), 0)
        self.assertEqual(swap_distance([0, 1, 2], [2, 1, 0]), 3)

    def test_swap_distance_between_potes(self):
        self.assertEqual(swap_distance_between_potes([0, 1, 2], [0, 1, 2]), 0)
        self.assertEqual(swap_distance_between_potes([0, 1, 2], [2, 1, 0]), 3)

    def test_spearman_distance_between_potes(self):
        self.assertEqual(spearman_distance_between_potes([0, 1, 2], [0, 1, 2]), 0)
        self.assertEqual(spearman_distance_between_potes([0, 1, 2], [2, 1, 0]), 4)


if __name__ == '__main__':
    unittest.main()
