from .node import Node
from .edge import Edge
from .path import Path
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class Network:
    def __init__(self, edges):
        self.__edges = edges  # edge_id -> Edge object
        self.__paths = {}  # path_id -> Path object
        
    def buildPaths(self):
        # Reset
        self.__paths = {}

        # Build adjacency list: node_id → list of outgoing edges
        adj = {}
        for e in self.__edges.values():
            adj.setdefault(e.getSrcId(), []).append(e)

        # Get all node IDs that appear in edges
        nodes = set()
        for e in self.__edges.values():
            nodes.add(e.getSrcId())
            nodes.add(e.getSinkId())
        nodes = list(nodes)

        # BFS from every start node
        path_id = 0

        for start in nodes:
            queue = [(start, [])]   # (current_node, list_of_edges_used)

            while queue:
                curr, used_edges = queue.pop(0)

                # If path length >= 1 -> valid full path
                if used_edges:
                    p = Path(used_edges)
                    self.__paths[p.getId()] = p

                # No outgoing edges
                if curr not in adj:
                    continue

                # Explore edges
                for e in adj[curr]:
                    next_node = e.getSinkId()

                    # Prevent cycles
                    visited_nodes = {e.getSrcId() for e in used_edges}
                    visited_nodes.add(curr)
                    if next_node in visited_nodes:
                        continue
                    queue.append((next_node, used_edges + [e]))

        
    def buildIncidenceMatrix(self):
        edge_ids = list(self.__edges.keys())
        path_ids = list(self.__paths.keys())
        
        m = len(edge_ids)
        n = len(path_ids)
        
        A = np.zeros((m, n), dtype=int)
        
        edge_index = {eid: i for i, eid in enumerate(edge_ids)}
        
        for j, pid in enumerate(path_ids):
            path = self.__paths[pid]
            for edge in path.getEdges():
                i = edge_index[edge.getId()]
                A[i, j] = 1
                
        return A
    

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

        plt.title("Traffic Network Graph")
        plt.axis('off')
        plt.show()
