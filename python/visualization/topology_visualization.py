from math import inf

import networkx as nx
import matplotlib.pyplot as plt

from typing import Dict, Tuple, List
from networkx import Graph
from matplotlib.backends.backend_pdf import PdfPages

from lib.topology import Topology, Link


def visualize_topology(topo: Topology, color_per_prio_dict: Dict[Link, float], pos: dict = None, filepath = "/tmp/last_topo.pdf", title = "", mincolor = -1, maxcolor = -1):
    G, pos2 = topo_to_graph(topo)
    if pos == None:
        pos = pos2

    with PdfPages(filepath) as pdf:
        mincolor, maxcolor, colors = edge_colors(G, color_per_prio_dict, mincolor, maxcolor)

        options = {
            "node_size": [
                180 if n["origin"].type == "switch" else 60
                for n in G._node.values()
            ],
            "node_color": [
                "#EEEEEE" if n["origin"].type == "switch" else "#3297a8"
                for n in G._node.values()
            ],
            "edgecolors": "#777777",
            "edge_color": colors,
            "linewidths": 1,
            "width": 1,
            "with_labels": False,
        }

        nx.draw(G, pos, **options)

        labels = {
            n.name: "x" if n.joinPoint else ""
            for n in topo.nodes
        }
        nx.draw_networkx_labels(G, pos, labels, font_size = 8, font_color = "#555555")

        plt.title(f"{title}\nmin={convert_bps_to_str(mincolor)}   max={convert_bps_to_str(maxcolor)}")
        plt.axis("off")
        pdf.savefig()
        plt.close()


def edge_colors(G: Graph, delays: Dict[Link, float], mincolor = -1, maxcolor = -1) -> Tuple[float, float, List[Tuple]]:
    # convert for compatibility with Graph
    # also combine both directions of a link to the same value, for simplicity
    delays = {l.name: max(t, delays[l.mirror()]) for l, t in delays.items()}

    # define green and red borders
    ret = []
    if mincolor == -1:
        mincolor = min(delays.values())
    if maxcolor == -1:
        maxcolor = max(delays.values())

    # convert delay values to colors
    for e in G.edges():
        if mincolor == maxcolor:
            pct = 0
        else:
            delay = delays["%s-%s" % (e[0], e[1])]
            pct = (delay - mincolor) / (maxcolor - mincolor)
        pctd = 1.0 - pct
        r = min(1, pct * 2)
        g = min(1, pctd * 2)
        ret.append((r, g, 0))

    return mincolor, maxcolor, ret


def topo_to_graph(topo: Topology) -> Tuple[Graph, dict]:
    G = nx.Graph()

    for n in topo.nodes:
        G.add_node(n.name)
        # save pointer to original object for easy access
        G.nodes[n.name]["origin"] = n

    for l in topo.links:
        if (l.n2.name, l.n1.name) not in G.edges:
            G.add_edge(l.n1.name, l.n2.name)
            G.edges[(l.n1.name, l.n2.name)]["origin"] = l

    pos = nx.spring_layout(G, k=0.9, iterations=2000)

    return G, pos


def convert_bps_to_str(bps: float) -> str:
    if bps > 1e9:
        return "%.2fGbit/s" % (bps / 1e9)
    if bps > 1e6:
        return "%.2fMbit/s" % (bps / 1e6)
    if bps > 1e3:
        return "%.2fkbit/s" % (bps / 1e3)
    return "%.2fbit/s" % (bps)
