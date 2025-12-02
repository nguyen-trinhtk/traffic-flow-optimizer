from network_model.node import Node
from network_model.edge import Edge
from network_model.network import Network
from setup import *

def build_test_network():
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

    edges = {
        e1.getId(): e1,
        e2.getId(): e2,
        e3.getId(): e3,
        e4.getId(): e4,
        e5.getId(): e5,
        e6.getId(): e6,
        e7.getId(): e7,
        e8.getId(): e8,
    }

    net = Network(edges)
    net.buildPaths()

    return net, edges

def main():
    net, edges = build_test_network()
    A_LP, b_LP, p_LP = prepare_lp_data(net, edges)
    print("\nLP Solution:")
    print(run_lp(A_LP, b_LP, p_LP))

if __name__ == "__main__":
    main()
