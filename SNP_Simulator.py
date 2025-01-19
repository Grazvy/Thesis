from utils import build_graph

import networkx as nx

# static n-player simulator
class SNP_Simulator():

    def __init__(self):
        self.frac = 0.5
        self.G = build_graph()
        self.labels = self.get_labels()
        self.progress = self.get_path_structure()

    def get_labels(self):
        multipliers = nx.get_edge_attributes(self.G, 'mult')
        constants = nx.get_edge_attributes(self.G, 'const')

        def label(mult, const):
            if mult == 0:
                return "0" if (const == 0) else f"{const}"
            elif mult == 1:
                return f"x" if (const == 0) else f"x + {const}"
            else:
                return f"{mult}x" if (const == 0) else f"{mult}x + {const}"

        edge_labels = {
            edge: label(multipliers[edge], constants[edge])
            for edge in self.G.edges
        }

        return edge_labels

    def get_path_structure(self):
        paths = list(nx.all_simple_paths(self.G, source='A', target='D'))
        structure = []  # (cost_per_fraction, const, flow)

        for path in paths:
            cpf = 0
            const = 0

            for u, v in nx.utils.pairwise(path):
                cpf += self.G.edges[u, v]['mult'] * self.frac
                const += self.G.edges[u, v]['const']

            structure.append((cpf, const, 0))

        return structure
