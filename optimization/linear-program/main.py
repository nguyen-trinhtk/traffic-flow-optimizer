from network_model.node import Node
from network_model.edge import Edge
from network_model.path import Path
from network_model.network import Network
from lp_solver import LPSolver
import numpy as np

def main():
    # -------------------- Build network --------------------
    n1 = Node()
    n2 = Node()
    n3 = Node()
    n4 = Node()
    n5 = Node()
    n6 = Node()

    e1 = Edge(n1, n2, 3)
    e2 = Edge(n2, n3, 5)
    e3 = Edge(n1, n3, 6)
    e4 = Edge(n3, n4, 7)
    e5 = Edge(n2, n5, 1)
    e6 = Edge(n5, n4, 2)
    e7 = Edge(n4, n6, 10)
    e8 = Edge(n5, n6, 9)

    p1 = Path([e1, e2, e4, e7])
    p2 = Path([e3, e4, e7])
    p3 = Path([e1, e5, e6, e8])
    p4 = Path([e1, e5, e8])

    net = Network()
    for edge in [e1, e2, e3, e4, e5, e6, e7, e8]:
        net.addEdge(edge)
    for path in [p1, p2, p3, p4]:
        net.addPath(path)

    # -------------------- Incidence matrix --------------------
    A = net.buildIncidenceMatrix()  # m x n (edges x paths)
    # print("Incidence Matrix (rows=edges, columns=paths):")
    # print(A)

    m, n = A.shape

    # -------------------- Build LP matrices --------------------
    # Capacities
    b = np.array([edge.getCapacity() for edge in [e1,e2,e3,e4,e5,e6,e7,e8]])

    # Flow thresholds for utility function, over = congestion
    c = np.array([5, 5, 5, 5])  # example ck for each path

    # Variables z = [x1..xn, y1..yn], total 2n
    # Constraint 1: Ax <= b (extend to include y variables)
    A1 = np.hstack([A, np.zeros((m, n))])
    b1 = b

    # Constraint 2: y_k <= x_k -> -x_k + y_k <= 0
    A2 = np.hstack([-np.eye(n), np.eye(n)])
    b2 = np.zeros(n)

    # Constraint 3: y_k <= 0.5 x_k + 0.5 c_k -> -0.5 x_k + y_k <= 0.5 c_k
    A3 = np.hstack([-0.5 * np.eye(n), np.eye(n)])
    b3 = 0.5 * c

    # Stack all constraints
    A_LP = np.vstack([A1, A2, A3])
    b_LP = np.hstack([b1, b2, b3])

    # Objective: maximize sum(y_k) -> f^T z
    p_LP = np.hstack([np.zeros(n), np.ones(n)])

    # print("\nLP matrix A_LP:")
    # print(A_LP)
    # print("\nLP vector b_LP:")
    # print(b_LP)
    # print("\nLP objective vector f (maximize sum of y):")
    # print(p_LP)
    
    solver = LPSolver(A_LP,b_LP,p_LP)
    print(solver.solveMaxLE())
    

if __name__ == "__main__":
    main()
