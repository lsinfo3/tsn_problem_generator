import random
from typing import Literal

from lib.topology import Topology, Host, Controller
from lib.y_random_util import unpack_random as ur, urandom_float_between
from stream_factory.create_streams import create_streams_for_topology
from topology_factory.combine_topologies import combine_topologies
from topology_factory.linear_branches import linear_branches
from topology_factory.two_layer_tree import two_layer_tree


def industrial_scenario(size: Literal["small", "medium", "big"]) -> Topology:
    sizes = ["small", "medium", "big"]
    if size not in sizes:
        raise ValueError(f"size may only be one of {sizes}, not '{size}'")



    if size == "small":
        topo = linear_branches(main_length=[2,5], branches_per_main_switch=1, branch_length=[1,3], hosts_per_branch_switch=[3,6], main_link_speed=1e9, branch_link_speed=1e8, connect_to_ring={True, False}, num_join_points=2)

        streams = []
        streams += create_streams_for_topology(topo, num_streams=30, burst_range=[64 * 8, 1000 * 8], rate_range=[10e3, 50e6, "log"], prio_range=[4, 7], max_pathlen=2)
        streams += create_streams_for_topology(topo, num_streams=30, burst_range=[64 * 8, 1000 * 8], rate_range=[10e3, 50e6, "log"], prio_range=[4, 7], min_pathlen=3, max_pathlen=3)
        streams += create_streams_for_topology(topo, num_streams=20,  burst_range=[64 * 8, 1000 * 8], rate_range=[10e3, 50e6, "log"], prio_range=[4, 7], min_pathlen=4, max_pathlen=4)
        streams += create_streams_for_topology(topo, num_streams=15,  burst_range=[64 * 8, 1000 * 8], rate_range=[10e3, 50e6, "log"], prio_range=[4, 7], min_pathlen=5, max_pathlen=5)
        streams += create_streams_for_topology(topo, num_streams=10,  burst_range=[64 * 8, 1000 * 8], rate_range=[10e3, 50e6, "log"], prio_range=[4, 7], min_pathlen=6, max_pathlen=6)
        streams += create_streams_for_topology(topo, num_streams=5,  burst_range=[64 * 8, 1000 * 8], rate_range=[10e3, 50e6, "log"], prio_range=[4, 7], min_pathlen=7, max_pathlen=7)
        topo.add_streams(streams)


    elif size == "medium":
        main_length = ur([3,5])
        topo = linear_branches(main_length=main_length, branches_per_main_switch=0, branch_length=0, hosts_per_branch_switch=0, main_link_speed=1e10, branch_link_speed=1e9, connect_to_ring=True, num_join_points=main_length)

        num_branches = -1
        while main_length > 0:
            num_branches += 1

            join_points = ur([1,2])
            while join_points > main_length: join_points = ur([1,2])
            main_length -= join_points

            topo2 = linear_branches(main_length=[2,4], branches_per_main_switch=1, branch_length=[1,3], hosts_per_branch_switch=[3,6], main_link_speed=1e9, branch_link_speed=1e8, connect_to_ring={True, False}, num_join_points=join_points).reset_with_prefix(f"r{num_branches}_")
            topo = combine_topologies(topo, topo2, add_name_prefixes=False, removeJoinPointsUsed=True, removeJoinPointsTopo2=True)

        # Connect 2 dangling switches with chance 10%
        if urandom_float_between(0, 1) >= 0.1:
            print("  -> Combining dangling switches...")
            dangling = topo.getDanglingSwitches()
            if len(dangling) >= 2:
                n1, n2 = random.sample(dangling, 2)
                print(f"    --> {n1.name}, {n2.name}")
                n1.addNeigh(n2, 1e8)

        streams = []
        streams += create_streams_for_topology(topo, num_streams=70, burst_range=[64 * 8, 1000 * 8], rate_range=[10e3, 50e6, "log"], prio_range=[4, 7], max_pathlen=2)
        streams += create_streams_for_topology(topo, num_streams=50, burst_range=[64 * 8, 1000 * 8], rate_range=[10e3, 50e6, "log"], prio_range=[4, 7], min_pathlen=3, max_pathlen=3)
        streams += create_streams_for_topology(topo, num_streams=40, burst_range=[64 * 8, 1000 * 8], rate_range=[10e3, 50e6, "log"], prio_range=[4, 7], min_pathlen=4, max_pathlen=4)
        streams += create_streams_for_topology(topo, num_streams=30, burst_range=[64 * 8, 1000 * 8], rate_range=[10e3, 50e6, "log"], prio_range=[4, 7], min_pathlen=5, max_pathlen=5)
        streams += create_streams_for_topology(topo, num_streams=20, burst_range=[64 * 8, 1000 * 8], rate_range=[10e3, 50e6, "log"], prio_range=[4, 7], min_pathlen=6, max_pathlen=6)
        streams += create_streams_for_topology(topo, num_streams=10, burst_range=[64 * 8, 1000 * 8], rate_range=[10e3, 50e6, "log"], prio_range=[4, 7], min_pathlen=7, max_pathlen=7)
        topo.add_streams(streams)


    else:  # big
        main_length = ur([4,6])
        topo = linear_branches(main_length=main_length, branches_per_main_switch=0, branch_length=0, hosts_per_branch_switch=0, main_link_speed=1e10, branch_link_speed=1e9, connect_to_ring=True, num_join_points=main_length)

        topo2 = two_layer_tree(num_layer1_switches=2, num_layer2_switches=[3,5], hosts_per_l2switch=[4,16], switch_link_speed=1e10, host_link_speed=1e9).reset_with_prefix("tree_")
        topo = combine_topologies(topo, topo2, add_name_prefixes=False, removeJoinPointsUsed=True, removeJoinPointsTopo2=True)
        main_length -= 2

        num_branches = -1
        while main_length > 0:
            num_branches += 1

            join_points = ur([1,2])
            while join_points > main_length: join_points = ur([1,2])
            main_length -= join_points

            topo2 = linear_branches(main_length=[2,5], branches_per_main_switch=[1,2], branch_length=[1,4], hosts_per_branch_switch=[3,6], main_link_speed=ur({1e9, 2.5e9}), branch_link_speed=1e8, connect_to_ring={True, False}, num_join_points=join_points).reset_with_prefix(f"r{num_branches}_")
            topo = combine_topologies(topo, topo2, add_name_prefixes=False, removeJoinPointsUsed=True, removeJoinPointsTopo2=True)

        # Connect 2 dangling switches with chance 50%
        if urandom_float_between(0, 1) >= 0.5:
            print("  -> Combining dangling switches...")
            dangling = topo.getDanglingSwitches()
            if len(dangling) >= 2:
                n1, n2 = random.sample(dangling, 2)
                print(f"    --> {n1.name}, {n2.name}")
                n1.addNeigh(n2, 1e8)

        streams = []
        streams += create_streams_for_topology(topo, num_streams=100, burst_range=[64 * 8, 1000 * 8], rate_range=[10e3, 50e6, "log"], prio_range=[4, 7], max_pathlen=2)
        streams += create_streams_for_topology(topo, num_streams=100, burst_range=[64 * 8, 1000 * 8], rate_range=[10e3, 50e6, "log"], prio_range=[4, 7], min_pathlen=3, max_pathlen=3)
        streams += create_streams_for_topology(topo, num_streams=80, burst_range=[64 * 8, 1000 * 8], rate_range=[10e3, 50e6, "log"], prio_range=[4, 7], min_pathlen=4, max_pathlen=4)
        streams += create_streams_for_topology(topo, num_streams=60, burst_range=[64 * 8, 1000 * 8], rate_range=[10e3, 50e6, "log"], prio_range=[4, 7], min_pathlen=5, max_pathlen=5)
        streams += create_streams_for_topology(topo, num_streams=50, burst_range=[64 * 8, 1000 * 8], rate_range=[10e3, 50e6, "log"], prio_range=[4, 7], min_pathlen=6, max_pathlen=6)
        streams += create_streams_for_topology(topo, num_streams=40, burst_range=[64 * 8, 1000 * 8], rate_range=[10e3, 50e6, "log"], prio_range=[4, 7], min_pathlen=7, max_pathlen=7)
        topo.add_streams(streams)


    return topo




def automotive_scenario():
    topo = linear_branches(main_length=[4, 6], branches_per_main_switch=1, branch_length=[4, 8], hosts_per_branch_switch=[2, 20, "log"], main_link_speed=10e9, branch_link_speed=1e9, connect_to_ring={True, False}, num_join_points=0)
    main_switches = [n for n in topo.nodes if "main_sw" in n.name]
    for n in main_switches:
        topo.create_and_add_links(n, Controller(f"HPC_{n.name}"), 10e9)

    # Connect 2 dangling switches with chance 50%
    if urandom_float_between(0, 1) >= 0.5:
        print("  -> Combining dangling switches...")
        dangling = topo.getDanglingSwitches()
        if len(dangling) >= 2:
            n1, n2 = random.sample(dangling, 2)
            print(f"    --> {n1.name}, {n2.name}")
            n1.addNeigh(n2, 1e9)

    # Connect another 2 dangling switches with chance 25%
    if urandom_float_between(0, 1) >= 0.25:
        print("  -> Combining dangling switches...")
        dangling = topo.getDanglingSwitches()
        if len(dangling) >= 2:
            n1, n2 = random.sample(dangling, 2)
            print(f"    --> {n1.name}, {n2.name}")
            n1.addNeigh(n2, 1e9)

    topo.add_streams(create_streams_for_topology(topo, num_streams=2*len(topo.sensors), burst_range=[64*8, 512*8], rate_range=[10e3, 50e6, "log"], prio_range=[4, 7], only_switch_controller_paths=True))

    return topo
