from math import inf

from export.to_json import to_json
from lib.z_test_util import link, get_tmp_filepath
from stream_factory.create_streams import create_streams_for_topology
from topology_factory.combine_topologies import combine_topologies
from topology_factory.linear_branches import linear_branches
from topology_factory.two_layer_tree import two_layer_tree
from visualization.topology_visualization import topo_to_graph, visualize_topology



if __name__ == '__main__':
    #topo2 = linear_branches(main_length=3, branches_per_main_switch=2, branch_length=2, hosts_per_branch_switch=3, main_link_speed=1e10, branch_link_speed=1e8, connect_to_ring=False, num_join_points=2)
    topo1 = linear_branches(main_length=6, branches_per_main_switch=1, branch_length=2, hosts_per_branch_switch=4, main_link_speed=1e10, branch_link_speed=1e8, connect_to_ring=True, num_join_points=2)
    #topo2 = linear_branches(main_length=6, branches_per_main_switch=1, branch_length=2, hosts_per_branch_switch=4, main_link_speed=1e10, branch_link_speed=1e8, connect_to_ring=True, num_join_points=2)
    topo2 = two_layer_tree(num_layer1_switches=2, num_layer2_switches=4, hosts_per_l2switch=12, switch_link_speed=1e10, host_link_speed=1e9)

    topo = combine_topologies(topo1, topo2, add_name_prefixes=True)

    streams = []
    streams += create_streams_for_topology(topo, num_streams=150, burst_range=[64 * 8, 1000 * 8], rate_range=[10e3, 50e6, "log"], prio_range=[4, 7], max_pathlen=2)
    streams += create_streams_for_topology(topo, num_streams=150, burst_range=[64 * 8, 1000 * 8], rate_range=[10e3, 50e6, "log"], prio_range=[4, 7], min_pathlen=3, max_pathlen=3)
    streams += create_streams_for_topology(topo, num_streams=75, burst_range=[64 * 8, 1000 * 8], rate_range=[10e3, 50e6, "log"], prio_range=[4, 7], min_pathlen=4, max_pathlen=4)
    streams += create_streams_for_topology(topo, num_streams=75, burst_range=[64 * 8, 1000 * 8], rate_range=[10e3, 50e6, "log"], prio_range=[4, 7], min_pathlen=5, max_pathlen=5)
    streams += create_streams_for_topology(topo, num_streams=75, burst_range=[64 * 8, 1000 * 8], rate_range=[10e3, 50e6, "log"], prio_range=[4, 7], min_pathlen=6, max_pathlen=6)
    streams += create_streams_for_topology(topo, num_streams=25, burst_range=[64 * 8, 1000 * 8], rate_range=[10e3, 50e6, "log"], prio_range=[4, 7], min_pathlen=7, max_pathlen=7)

    topo.add_streams(streams)

    # prio = (0,   1,   2,   3,   4,    5,    6,     7    )
    per_hop_guarantees = (inf, inf, inf, inf, 50e6, 10e6, 500e3, 150e3)
    topo.update_guarantees_all_links(per_hop_guarantees)

    # prio = (0,   1,   2,   3,   4,     5,     6,     7    )
    idle_slopes = (inf, inf, inf, inf, 100e6, 100e6, 100e6, 50e6)
    topo.update_idle_slopes_all_links(idle_slopes)

    JSON_FILE = get_tmp_filepath("problem_gen/json-test.json")
    PDF_FILE = get_tmp_filepath("problem_gen/pdf-test.pdf")

    to_json(topo, JSON_FILE)
    print(f"Exported JSON to {link(JSON_FILE)}")

    bw_dict = {l: l.bandwidth for l in topo.links}
    _, positions = topo_to_graph(topo)
    visualize_topology(topo, bw_dict, pos=positions, filepath=PDF_FILE, title="Topology bandwidth overview")
    print(f"Exported Visualization to {link(PDF_FILE)}")