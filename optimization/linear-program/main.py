# main.py
from setUp import nodes, edges, sources, sinks
from solve import solve_traffic_lp
from graph import plot_graph

def main():
    flows, timings = solve_traffic_lp(nodes, edges, sources, sinks)
    
    print("Optimal traffic signal timings:")
    for n, t in timings.items():
        print(f"Node {n}: t = {t:.2f}")
    
    print("\nOptimal flows on edges:")
    for e, f in flows.items():
        print(f"Edge {e}: flow = {f:.2f}")
    
    plot_graph(nodes, edges, flows, title="Optimized Traffic Network")

if __name__ == "__main__":
    main()
