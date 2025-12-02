from .node import Node
from .edge import Edge
from .path import Path
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class Network:
    def __init__(self):
        self.__edges = {}  # edge_id -> Edge object
        self.__paths = {}  # path_id -> Path object
        
    def updateEdges(self, edgesMap):
        self.__edges.update(edgesMap)
        
    def addEdge(self, edge):
        self.__edges.update({edge.getId(): edge})
        
    def addPath(self, path):
        # check availability of edges
        for edge in path.getEdges():
            eid = edge.getId()
            if eid not in self.__edges:
                raise ValueError(f"Unknown edge: {eid}")
        self.__paths.update({path.getId(): path})
        
    def buildIncidenceMatrix(self):
        edge_ids = list(self.__edges.keys())
        path_ids = list(self.__paths.keys())
        
        m = len(edge_ids)
        n = len(path_ids)
        
        # Create a zero matrix of size m x n
        A = np.zeros((m, n), dtype=int)
        
        # Build a mapping from edge_id to row index
        edge_index = {eid: i for i, eid in enumerate(edge_ids)}
        
        # Build the incidence matrix
        for j, pid in enumerate(path_ids):
            path = self.__paths[pid]
            for edge in path.getEdges():
                i = edge_index[edge.getId()]
                A[i, j] = 1
                
        return A
    
    # ------------------ Interactive Visualizer ------------------
    def visualize(self):
        G = nx.DiGraph()

        for edge in self.__edges.values():
            start, end = edge.getSrcId(), edge.getSinkId()
            G.add_edge(start, end, id=edge.getId())
            
        pos = nx.spring_layout(G, seed=42)

        # Nodes & labels
        nx.draw_networkx_nodes(G, pos, node_color='lightgrey', node_size=600)
        nx.draw_networkx_labels(G, pos, labels={n: f"{n}" for n in G.nodes()}, font_size=12)

        # Edges & labels
        nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, edge_color='black', width=2)
        edge_labels = {(u, v): f"e{d['id']}" for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

        # TODO: path highlighting
        # colors = ['red', 'green', 'blue', 'orange', 'purple']
        # for idx, path in enumerate(self.__paths.values()):
        #     path_edges = [(e.getSrcId(), e.getSinkId()) for e in path.getEdges()]
        #     nx.draw_networkx_edges(
        #         G, pos,
        #         edgelist=path_edges,
        #         edge_color=colors[idx % len(colors)],
        #         width=3,
        #         arrowstyle='-|>',
        #         arrowsize=20
        #     )
        plt.title("Traffic Network Graph")
        plt.axis('off')
        plt.show()
