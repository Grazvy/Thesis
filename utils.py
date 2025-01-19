import networkx as nx
from matplotlib.patches import Rectangle

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

def draw_rect(ax, x, y, w=0.1, h=0.04):
    ax.add_patch(Rectangle((x, y), w, h, linewidth=1, edgecolor='b', facecolor='b'))

def interpolate_positions(pos, path_edges, steps):
    interpolated_positions = []
    for edge in path_edges:
        start, end = pos[edge[0]], pos[edge[1]]
        xs = [start[0] + (end[0] - start[0]) * t / steps for t in range(steps)]
        ys = [start[1] + (end[1] - start[1]) * t / steps for t in range(steps)]
        interpolated_positions.extend(zip(xs, ys))
    return interpolated_positions


def progress_bar(fraction, prefix="", length=40, fill="█"):
    fraction = max(0, min(1, fraction))
    percent = ("{0:.1f}").format(100 * fraction)
    filled_length = int(length * fraction)
    bar = fill * filled_length + "-" * (length - filled_length)
    print(f"\r{prefix} |{bar}| {percent}%", end="")


