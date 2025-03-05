import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FFMpegWriter


from utils import build_graph, interpolate_positions, draw_rect, progress_bar

CPF = 0
CONST = 1
FLOW = 2


# static n-player simulator
class SNP_Simulator:

    def __init__(self, total_flow=1, num_fractions=5):
        self.num_fractions = num_fractions
        self.frac = total_flow / num_fractions
        self.G = build_graph()
        self.paths = list(nx.all_simple_paths(self.G, source='A', target='D'))
        self.labels = self.get_labels()
        self.pos = nx.shell_layout(self.G)
        # self.pos = nx.spring_layout(G)

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

        return flow_order, induced_costs

    def save_results(self, order, fps=20, steps=5, width=10):
        metadata = dict(title="Network Animation", artist="Matplotlib", comment="Path traversal animation")
        writer = FFMpegWriter(fps=fps, metadata=metadata)
        fig, ax = plt.subplots(figsize=(width, 6))
        info_ax = fig.add_axes([0.85, 0.1, 0.1, 0.8])
        sx, sy = self.pos['A']
        tx, ty = self.pos['D']
        h = 0.2 / self.num_fractions
        progress = self.get_path_structure()

        with writer.saving(fig, "network_animation.mp4", dpi=100):
            for i, path_index in enumerate(order):
                point_positions = interpolate_positions(self.pos, list(nx.utils.pairwise(self.paths[path_index])), steps)
                progress_bar(i / len(order))
                progress[path_index][CONST] += progress[path_index][CPF]

                info_ax.clear()
                info_ax.axis('off')
                info_ax.text(0.6, 1.05, "Path costs", ha='center', va='top', fontsize=12, fontweight='bold')
                for j, path in enumerate(progress):
                    label = "-".join(map(str, self.paths[j]))
                    info_ax.text(0.6, 0.9 - 0.15 * j, f"{label} : {round(path[CONST], 3)}", ha='center', fontsize=10)

                # make frame
                for x, y in point_positions:
                    ax.clear()
                    nx.draw(self.G, self.pos, with_labels=True, node_color="gray", edge_color="gray", node_size=300,
                            font_size=10, font_weight="bold", ax=ax)
                    nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=self.labels, font_size=15, ax=ax)
                    ax.plot(x - 0.02, y, "bs", markersize=6)

                    draw_rect(ax, x=(sx - 0.05), y=(sy + 0.15), h=h * (self.num_fractions - i - 1))
                    if i != 0:
                        draw_rect(ax, x=(tx - 0.05), y=(ty + 0.15), h=h * i)

                    writer.grab_frame()
                    plt.close(fig)

            ax.clear()
            nx.draw(self.G, self.pos, with_labels=True, node_color="gray", edge_color="gray", node_size=300,
                    font_size=10, font_weight="bold", ax=ax)
            nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=self.labels, font_size=15, ax=ax)
            draw_rect(ax, x=(tx - 0.05), y=(ty + 0.15), h=h * i)
            writer.grab_frame()
            plt.close(fig)
            progress_bar(1)

        print("\nVideo file saved as network_animation.mp4")

    def plot_network(self):
        nx.draw(self.G, self.pos, with_labels=True, node_color="skyblue", node_size=300, font_size=10, font_weight="bold",
                edge_color="gray", width=5)
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=self.labels, font_size=15)

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
        structure = []  # (cost_per_fraction, const, flow)

        for path in self.paths:
            cpf = 0
            const = 0

            for u, v in nx.utils.pairwise(path):
                cpf += self.G.edges[u, v]['mult'] * self.frac
                const += self.G.edges[u, v]['const']

            structure.append([cpf, const, 0])

        return structure
