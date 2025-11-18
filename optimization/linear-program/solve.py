# Solve LP
# solve.py
import pulp

def solve_traffic_lp(nodes, edges, sources, sinks):
    prob = pulp.LpProblem("TrafficSignalOptimization", pulp.LpMaximize)

    x = {e: pulp.LpVariable(f"x_{e[0]}_{e[1]}", lowBound=0) for e in edges}
    t = {n: pulp.LpVariable(f"t_{n}", lowBound=0, upBound=1) for n in nodes}

    prob += pulp.lpSum(x[e] for e in edges if e[0] in sources)

    for (i,j), cap in edges.items():
        prob += x[(i,j)] <= cap * t[i]

    internal_nodes = [n for n in nodes if n not in sources+sinks]
    for n in internal_nodes:
        incoming = [x[(i,j)] for (i,j) in edges if j==n]
        outgoing = [x[(i,j)] for (i,j) in edges if i==n]
        prob += pulp.lpSum(incoming) == pulp.lpSum(outgoing)


    prob.solve()

    flow_solution = {e: x[e].varValue for e in edges}
    timing_solution = {n: t[n].varValue for n in nodes}

    return flow_solution, timing_solution
