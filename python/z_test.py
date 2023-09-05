import os

from factory_profiles.scenario_factory_profiles import industrial_scenario, automotive_scenario
from lib.z_test_util import link, get_tmp_filepath
from visualization.topology_visualization import topo_to_graph, visualize_topology, graph_positions

HOW_MANY = 20
#SCENARIO = "industrial"
SCENARIO = "automotive"
SIZE = "big"
PDFS = []
REMOVE_SMALL_PDFs = True


if __name__ == '__main__':
    for i in range(HOW_MANY):
        print(f"Generating topology {i+1}/{HOW_MANY} ({SCENARIO}, size {SIZE}) ...")

        if SCENARIO == "industrial":
            topo = industrial_scenario(SIZE)
        elif SCENARIO == "automotive":
            topo = automotive_scenario()
        else:
            raise ValueError(f"scenario {SCENARIO} unknown")

        JSON_FILE = get_tmp_filepath("problem_gen/json.json")
        #to_json(topo, JSON_FILE)
        #print(f"  Exported JSON to {link(JSON_FILE)}")

        for colorization in ["bw", "burst"]:
            PDF_FILE = get_tmp_filepath(f"problem_gen/pdf-{colorization}.pdf")
            PDFS += [PDF_FILE]
            pos = graph_positions(topo_to_graph(topo))

            # link color selection
            if colorization == "bw":
                bw_dict = {l: l.bandwidth for l in topo.links}
                visualize_topology(topo, bw_dict, pos=pos, filepath=PDF_FILE, title="Topology bandwidth overview")
            elif colorization == "burst":
                burst_dict = {l: sum([s.burst for s in topo.streams_per_link.get(l, dict()).values()]) / l.bandwidth * 1e9 for l in topo.links}
                visualize_topology(topo, burst_dict, pos=pos, filepath=PDF_FILE, title="Topology burst overview")

            #print(f"  Exported Visualization to {link(PDF_FILE)}")

        #print(f"  -> centrality = {np.mean([x for x in nx.degree_centrality(G).values()])}")
        #print(f"  -> betweenness = {np.mean([x for x in nx.betweenness_centrality(G).values()])}")

    JOINED_PDF = get_tmp_filepath(f"problem_gen/pdf-test-{SCENARIO}-{SIZE}-{HOW_MANY}.pdf")
    os.system(f"pdfunite {' '.join(PDFS)} {JOINED_PDF}")
    print(f"United PDFs to {link(JOINED_PDF)} ...")

    if REMOVE_SMALL_PDFs:
        for pdf in PDFS:
            os.remove(pdf)





    # topo = two_layer_tree(num_layer1_switches=2, num_layer2_switches=4, hosts_per_l2switch=8, switch_link_speed=1e10, host_link_speed=1e9)
    # bw_dict = {l: l.bandwidth for l in topo.links}
    # G, positions = topo_to_graph(topo)
    # PDFS = []
    # for layout in "dot".split():
    #     #positions = graphviz_layout(G, prog=layout, args="")
    #     positions = {}
    #     w = 3000
    #     for i in range(2):
    #         y = 150
    #         x = [1200, 1800][i]
    #         positions[f'sw_l1_{i}'] = (x,y)
    #         for j in range(2):
    #             y2 = 100
    #             x2 = x + [-150, +150][j]
    #             positions[f'sw_l2_{i * 2 + j}'] = (x2,y2)
    #             for k in range(8):
    #                 y3 = 50
    #                 x3 = x2 + [-105, -75, -45, -15, +15, +45, +75, +105][k]
    #                 positions[f'd_{i * 2 + j}_{k}'] = (x3,y3)
    #     pprint(positions)
    #     PDF_FILE = get_tmp_filepath(f"problem_gen/pdf-test-{layout}.pdf")
    #     PDFS.append(PDF_FILE)
    #     visualize_topology(topo, bw_dict, pos=positions, filepath=PDF_FILE, title="Topology bandwidth overview")
    #     print(f"  Exported Visualization to {link(PDF_FILE)}")
    # JOINED_PDF = get_tmp_filepath(f"problem_gen/pdf-test-united-graphviz-tree.pdf")
    # os.system(f"pdfunite {' '.join(PDFS)} {JOINED_PDF}")
    # print(f"United PDFs to {link(JOINED_PDF)} ...")
