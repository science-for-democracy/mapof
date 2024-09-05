import numpy as np

from mapof.core.inner_distances import l1, l2

VECTOR_1 = np.array([7,2,3,4,1,1])
VECTOR_2 = np.array([2,3,2,5,3,3])


def test_l1_inner_distances(tmp_path):
  v1 = VECTOR_1
  v2 = VECTOR_2
  assert l1(v1, v2) == 12


def test_l2_inner_distances():
  v1 = VECTOR_1
  v2 = VECTOR_2
  assert l2(v1, v2) == 6.
