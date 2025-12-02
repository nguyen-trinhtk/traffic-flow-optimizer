from network_model.node import Node
from network_model.edge import Edge
from network_model.network import Network
from lp_solver import LPSolver
import numpy as np
def prepare_lp_data(net, edges):

    A = net.buildIncidenceMatrix()
    print("Incidence Matrix:")
    print(A)

    m, n = A.shape
    print(f"\nEdges = {m}, Paths = {n}")

    # capacities
    edge_order = [edges[i] for i in sorted(edges)]
    b = np.array([e.getCapacity() for e in edge_order])

    # congestion threshold
    c = np.full(n, 5)

    # Ax <= b (introduce slack variables)
    A1 = np.hstack([A, np.zeros((m, n))])
    b1 = b

    # y <= x  → -x + y <= 0
    A2 = np.hstack([-np.eye(n), np.eye(n)])
    b2 = np.zeros(n)

    # y <= 0.5 x + 0.5 c
    A3 = np.hstack([-0.5 * np.eye(n), np.eye(n)])
    b3 = 0.5 * c

    # Combine
    A_LP = np.vstack([A1, A2, A3])
    b_LP = np.hstack([b1, b2, b3])

    # Objective: maximize sum(y)
    p_LP = np.hstack([np.zeros(n), np.ones(n)])

    return A_LP, b_LP, p_LP

def run_lp(A_LP, b_LP, p_LP):
    solver = LPSolver(A_LP, b_LP, p_LP)
    return solver.solveMaxLE()