from typing import Union, List, Tuple, Set

from lib.topology import Topology, Switch, Host
from lib.y_random_util import unpack_random as ur

MyRangeType = Union[int, float, List, Tuple, Set]


def two_layer_tree(num_layer1_switches: MyRangeType, num_layer2_switches: MyRangeType, hosts_per_l2switch: MyRangeType, switch_link_speed: MyRangeType, host_link_speed: MyRangeType) -> Topology:
    topo = Topology()

    # Create switches
    layer1_switches = [topo.add_node(Switch("sw_l1_0"))]
    for i in range(1, ur(num_layer1_switches)):
        layer1_switches.append(topo.create_and_add_links(layer1_switches[-1], Switch(f"sw_l1_{i}"), ur(switch_link_speed)))

    layer2_switches = [topo.add_node(Switch("sw_l2_0"))]
    for i in range(1, ur(num_layer2_switches)):
        layer2_switches.append(topo.create_and_add_links(layer2_switches[-1], Switch(f"sw_l2_{i}"), ur(switch_link_speed)))

    for sw1 in layer1_switches:
        for sw2 in layer2_switches:
            sw1.addNeigh(sw2, ur(switch_link_speed))

    # Create hosts
    for l2i, sw2 in enumerate(layer2_switches):
        for i in range(ur(hosts_per_l2switch)):
            topo.create_and_add_links(sw2, Host(f"d_{l2i}_{i}"), ur(host_link_speed))

    # Join points for topology fusion; select all l1 switches
    for sw1 in layer1_switches:
        sw1.joinPoint = True

    return topo
