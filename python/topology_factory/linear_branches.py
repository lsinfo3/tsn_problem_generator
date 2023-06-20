import random

from lib.topology import Topology, Switch, Host


def linear_branches(main_length: int, branches_per_main_switch: int, branch_length: int, hosts_per_branch_switch: int, main_link_speed: float, branch_link_speed: float, connect_to_ring: bool = False, num_join_points: int = 0) -> Topology:
    topo = Topology()

    # Create main switches
    main_switches = [topo.add_node(Switch("main_sw0"))]
    for i in range(1, main_length):
        main_switches.append(topo.create_and_add_links(main_switches[-1], Switch(f"main_sw{i}"), main_link_speed))

    # Are we creating a line or a ring?
    if connect_to_ring:
        main_switches[0].addNeigh(main_switches[-1], main_link_speed)

    # Join points for topology fusion; select random switches from the main line
    for i in random.sample(range(len(main_switches)), num_join_points):
        main_switches[i].joinPoint = True

    # Create branch switches and end devices
    for i, sw in enumerate(main_switches):
        for j in range(branches_per_main_switch):
            branch_switches = [topo.create_and_add_links(sw, Switch(f"branch_{i}.{j}_sw0"), branch_link_speed)]
            for l in range(hosts_per_branch_switch):
                topo.create_and_add_links(branch_switches[-1], Host(f"d_{i}.{j}.0_{l}"), branch_link_speed)
            for k in range(1, branch_length):
                branch_switches.append(topo.create_and_add_links(branch_switches[-1], Switch(f"branch_{i}.{j}_sw{k}"), branch_link_speed))
                for l in range(hosts_per_branch_switch):
                    topo.create_and_add_links(branch_switches[-1], Host(f"d_{i}.{j}.{k}_{l}"), branch_link_speed)

    return topo
