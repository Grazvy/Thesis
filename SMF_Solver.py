import networkx as nx
import numpy as np

from utils import build_graph, path_has_edge


def solve_static_meanfield():
    graph = build_graph()
    paths = list(nx.all_simple_paths(graph, source="A", target="D"))

    lh = np.array([np.ones(len(paths))])
    rh = np.array([1])
    costs = []

    for current in paths:
        const_cost = 0
        mult_cost = np.zeros(len(paths))

        for u, v in nx.utils.pairwise(current):
            const_cost += graph.edges[u, v]["const"]

            for i, path in enumerate(paths):
                if path_has_edge(path, u, v):
                    mult_cost[i] += graph.edges[u, v]["mult"]

        costs.append((mult_cost, const_cost))

    mult_trns, const_trns = costs[-1]
    for i in range(len(costs) - 1):
        mult, const = costs[i]
        lh = np.append(lh, [mult - mult_trns], axis=0)
        rh = np.append(rh, const_trns - const)

    try:
        np.linalg.solve(lh, rh)
        sol = np.linalg.solve(lh, rh)
        if any(x < 0 for x in sol):
            print("No valid solution found.")

        return sol
    except np.linalg.linalg.LinAlgError:
        print("An error occured while solving the linear equation system.")