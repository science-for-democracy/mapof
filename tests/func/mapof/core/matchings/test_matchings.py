import unittest
import numpy as np
from gurobipy import GRB
from mapof.core.matchings import *
from mapof.core.distances import single_l1

def l1_distance(x, y):
    return np.abs(x - y).sum()

class TestSolveMatching(unittest.TestCase):

    def test_solve_matching_vectors(self):
        # Test case 1: Simple 2x2 cost table
        cost_table = [[1, 2], [3, 4]]
        obj_val, matching = solve_matching_vectors(cost_table)
        self.assertEqual(obj_val, 5)  # Optimal assignment: (0,0) and (1,1)
        self.assertEqual(matching, [0, 1])

        # # Test case 2: Larger cost table
        cost_table = [[4, 1, 1], [2, 0, 5], [3, 2, 3]]
        obj_val, matching = solve_matching_vectors(cost_table)
        self.assertEqual(obj_val, 4)  # Optimal assignment: (0,2), (1,1), (2,0)
        self.assertEqual(matching, [2, 1, 0])

    def test_solve_matching_matrices(self):
        # Test case 1: Simple 2x2 matrices with L1 distance
        matrix_1 = [[0, 1], [2, 0]]
        matrix_2 = [[0, 4], [1, 0]]
        length = 2
        objective_value = solve_matching_matrices(matrix_1, matrix_2, length, single_l1)
        self.assertAlmostEqual(objective_value, 2)  # As matching identical entries costs 0 with L1

        # Test case 2: Slightly more complex 3x3 matrices with L1 distance
        matrix_1 = [[0, 2, 1], [3, 0, 4], [1, 5, 0]]
        matrix_2 = [[0, 5, 1], [3, 0, 4], [1, 2, 0]]
        length = 3
        objective_value = solve_matching_matrices(matrix_1, matrix_2, length, l1_distance)
        self.assertAlmostEqual(objective_value, 2)  # Expected value based on L1 calculation

if __name__ == "__main__":
    unittest.main()
