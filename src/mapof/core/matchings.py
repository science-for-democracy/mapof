import gurobipy as gp
import numpy as np
from gurobipy import GRB
from scipy.optimize import linear_sum_assignment


def solve_matching_vectors(cost_table: list[list]) -> (float, list):
    """
    Computes linear sum assignment.

    Parameters
    ----------
        cost_table : list[list]
            Cost table.
    Returns
    -------
        (float, list)
            Objective value, Optimal matching
    """

    cost_table = np.array(cost_table)
    row_ind, col_ind = linear_sum_assignment(cost_table)
    return cost_table[row_ind, col_ind].sum(), list(col_ind)


def solve_matching_matrices(
        matrix_1: list[list],
        matrix_2: list[list],
        length: int,
        inner_distance: callable
) -> float:
    """
    Computes the minimal distance between two matrices.

    We assume that both matrices are square matrices of the same size with zeros on the diagonal.

    We allow reordering of the rows and columns of the second matrix, however, whenever we reorder
     a row we have to reorder the corresponding column as well, and vice versa.

    We use the Gurobi optimization library to solve the assignment problem.

    Parameters
    ----------
        matrix_1 : list[list]
            First square matrix.
        matrix_2 : list[list]
            Second square matrix.
        length : int
            Length of the matrix.
        inner_distance : callable
            The inner distance (like L1 or L2).
    Returns
    -------
        float
            Objective value.
    """

    m = gp.Model()
    m.ModelSense = GRB.MINIMIZE

    # OBJECTIVE FUNCTION
    variables = {}
    for k in range(length):
        for l in range(length):
            for i in range(length):
                if i == k:
                    continue
                for j in range(length):
                    if j == l:
                        continue
                    weight = inner_distance(np.array([matrix_1[k][i]]), np.array([matrix_2[l][j]]))
                    name = f'Pk{k}l{l}i{i}j{j}'
                    variables[name] = m.addVar(vtype=GRB.BINARY, name=name, obj=weight)

    # ADD MISSING VARIABLES
    for i in range(length):
        for j in range(length):
            name = f'Mi{i}j{j}'
            variables[name] = m.addVar(vtype=GRB.BINARY, name=name)

    m.update()

    # CONSTRAINTS
    for k in range(length):
        for l in range(length):
            for i in range(length):
                if i == k:
                    continue
                for j in range(length):
                    if j == l:
                        continue

                    m.addConstr(variables[f'Pk{k}l{l}i{i}j{j}'] - variables[f'Mi{i}j{j}'] <= 0)
                    m.addConstr(variables[f'Pk{k}l{l}i{i}j{j}'] - variables[f'Mi{k}j{l}'] <= 0)

    for i in range(length):
        m.addConstr(gp.quicksum(variables[f'Mi{i}j{j}'] for j in range(length)) == 1)

    for j in range(length):
        m.addConstr(gp.quicksum(variables[f'Mi{i}j{j}'] for i in range(length)) == 1)

    for k in range(length):
        for i in range(length):
            if k == i:
                continue
            m.addConstr(gp.quicksum(variables[f'Pk{k}l{l}i{i}j{j}']
                                    for l in range(length)
                                    for j in range(length) if l != j) == 1)

    for l in range(length):
        for j in range(length):
            if l == j:
                continue
            m.addConstr(gp.quicksum(variables[f'Pk{k}l{l}i{i}j{j}']
                                    for k in range(length)
                                    for i in range(length) if k != i) == 1)

    # SOLVE THE ILP
    m.setParam('OutputFlag', 0)
    m.optimize()

    for var_name, var in variables.items():
        print(f"{var_name}: {var}")
    for constr in m.getConstrs():
        print(constr)

    if m.status == GRB.OPTIMAL:
        objective_value = m.objVal
        return objective_value
    else:
        print("Exception raised while solving")
