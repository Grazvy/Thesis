import networkx as nx

def build_graph():
    G = nx.DiGraph()
    G.add_nodes_from(["A", "C", "D", "B"])

    # costs affine linear: mult * x + const
    G.add_edge("A", "B", mult=1, const=0)
    G.add_edge("B", "D", mult=0, const=1)
    G.add_edge("A", "C", mult=0, const=1)
    G.add_edge("C", "D", mult=1, const=0)

    G.add_edge("B", "C", mult=0, const=0)

    return G

