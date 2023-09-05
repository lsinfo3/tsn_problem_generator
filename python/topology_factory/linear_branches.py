import random
from typing import Union, List, Tuple, Set

from lib.topology import Topology, Switch, Host, Sensor
from lib.y_random_util import unpack_random as ur

MyRangeType = Union[int, float, List, Tuple, Set]


def linear_branches(main_length: MyRangeType, branches_per_main_switch: MyRangeType, branch_length: MyRangeType, hosts_per_branch_switch: MyRangeType, main_link_speed: MyRangeType, branch_link_speed: MyRangeType, connect_to_ring: MyRangeType = False, num_join_points: MyRangeType = 0) -> Topology:
    topo = Topology()

    # Create main switches
    main_switches = [topo.add_node(Switch("main_sw0"))]
    for i in range(1, ur(main_length)):
        main_switches.append(topo.create_and_add_links(main_switches[-1], Switch(f"main_sw{i}"), ur(main_link_speed)))

    # Are we creating a line or a ring?
    if ur(connect_to_ring):
        main_switches[0].addNeigh(main_switches[-1], ur(main_link_speed))

    # Join points for topology fusion; select random switches from the main line
    for i in random.sample(range(len(main_switches)), min(len(main_switches), ur(num_join_points))):
        main_switches[i].joinPoint = True

    # Create branch switches and end devices
    for i, sw in enumerate(main_switches):
        for j in range(int(ur(branches_per_main_switch))):
            branch_switches = [topo.create_and_add_links(sw, Switch(f"branch_{i}.{j}_sw0"), ur(branch_link_speed))]
            for k in range(1, int(ur(branch_length))):
                branch_switches.append(topo.create_and_add_links(branch_switches[-1], Switch(f"branch_{i}.{j}_sw{k}"), ur(branch_link_speed)))
            for k, bsw in enumerate(branch_switches):
                for l in range(int(ur(hosts_per_branch_switch))):
                    topo.create_and_add_links(bsw, Sensor(f"d_main{i}.branch{j}_branchdepth{k}_dev{l}"), ur(branch_link_speed))

    return topo
