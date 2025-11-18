# Graph visualization for LPs
import networkx as nx
import matplotlib.pyplot as plt

def plot_graph(nodes, edges, flows=None, title="Traffic Network"):
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    for (i,j), cap in edges.items():
        label = f"{cap}"
        if flows and (i,j) in flows:
            label += f"\n({flows[(i,j)]:.0f})"
        G.add_edge(i, j, label=label)
    
    pos = nx.spring_layout(G, seed=42)
    edge_labels = nx.get_edge_attributes(G, 'label')
    
    plt.figure(figsize=(6,4))
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color='lightblue', arrowsize=20)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title(title)
    plt.show()
