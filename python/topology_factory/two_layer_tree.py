import random

from lib.topology import Topology, Switch, Host


def two_layer_tree(num_layer1_switches: int, num_layer2_switches: int, hosts_per_l2switch: int, switch_link_speed: float, host_link_speed: float) -> Topology:
    topo = Topology()

    # Create switches
    layer1_switches = [topo.add_node(Switch("sw_l1_0"))]
    for i in range(1, num_layer1_switches):
        layer1_switches.append(topo.create_and_add_links(layer1_switches[-1], Switch(f"sw_l1_{i}"), switch_link_speed))

    layer2_switches = [topo.add_node(Switch("sw_l2_0"))]
    for i in range(1, num_layer2_switches):
        layer2_switches.append(topo.create_and_add_links(layer2_switches[-1], Switch(f"sw_l2_{i}"), switch_link_speed))

    for sw1 in layer1_switches:
        for sw2 in layer2_switches:
            sw1.addNeigh(sw2, switch_link_speed)

    # Create hosts
    for l2i, sw2 in enumerate(layer2_switches):
        for i in range(hosts_per_l2switch):
            topo.create_and_add_links(sw2, Host(f"d_{l2i}_{i}"), host_link_speed)

    # Join points for topology fusion; select all l1 switches
    for sw1 in layer1_switches:
        sw1.joinPoint = True

    return topo
