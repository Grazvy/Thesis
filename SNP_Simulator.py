import matplotlib.pyplot as plt
import networkx as nx

from utils import build_graph

CPF = 0
CONST = 1
FLOW = 2


# static n-player simulator
class SNP_Simulator:

    def __init__(self, total_flow=1, num_fractions=5):
        self.num_fractions = num_fractions
        self.frac = total_flow / num_fractions
        self.G = build_graph()
        self.labels = self.get_labels()

    def run_simulation(self):
        progress = self.get_path_structure()
        flow_order = []

        for _ in range(self.num_fractions):
            direct_costs = [path[CPF] + path[CONST] for path in progress]
            i = direct_costs.index(min(direct_costs))

            progress[i][CONST] += progress[i][CPF]
            progress[i][FLOW] += self.frac
            flow_order.append(i)

        induced_costs = [path[CONST] * path[FLOW] for path in progress]

        return flow_order, max(induced_costs)

    def plot_results(self):
        #todo
        pass

    def plot_network(self):
        pos = nx.shell_layout(self.G)
        # pos = nx.spring_layout(G)

        nx.draw(self.G, pos, with_labels=True, node_color="skyblue", node_size=300, font_size=10, font_weight="bold",
                edge_color="gray", width=5)
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=self.labels, font_size=15)

        plt.title("Braess Network")
        plt.show()

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

            structure.append([cpf, const, 0])

        return structure
