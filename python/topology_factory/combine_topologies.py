import random
from math import inf

from lib.topology import Topology, Node


def combine_topologies(topo1: Topology, topo2: Topology, maxJoins: int = inf, add_name_prefixes: bool = True, removeJoinPointsUsed: bool = True, removeJoinPointsTopo1: bool = False, removeJoinPointsTopo2: bool = False) -> Topology:
    jps1 = topo1.joinPoints
    jps2 = topo2.joinPoints
    jpsl = min(maxJoins, len(jps1), len(jps2))

    if jpsl == 0:
        raise ValueError(f"at least one topology has no join points (topo1={len(jps1)}, topo2={len(jps2)})")

    # Prevent having the same node name twice
    if add_name_prefixes:
        prefix1 = "t1_"
        prefix2 = "t2_"
    else:
        prefix1 = ""
        prefix2 = ""

        names1 = set(n.name for n in topo1.nodes)
        names2 = set(n.name for n in topo2.nodes)
        names3 = names1.union(names2)

        if len(names1) + len(names2) != len(names3):
            raise ValueError(f"The names of both topologies are not mutually exclusive - consider using `add_name_prefixes`")

    jpr1 = random.sample(jps1, k=jpsl)
    jpr2 = random.sample(jps2, k=jpsl)

    new_topo = Topology()
    for n in topo1.nodes:
        nn = Node(name=f"{prefix1}{n.name}", type=n.type, joinPoint=n.joinPoint)
        n.nn = nn
        new_topo.add_node(nn)
    for n in topo2.nodes:
        nn = Node(name=f"{prefix2}{n.name}", type=n.type, joinPoint=n.joinPoint)
        n.nn = nn
        new_topo.add_node(nn)

    for l in topo1.links:
        l.n1.nn.addNeigh(l.n2.nn, bw=l.bandwidth)
    for l in topo2.links:
        l.n1.nn.addNeigh(l.n2.nn, bw=l.bandwidth)

    for jp1, jp2 in zip(jpr1, jpr2):
        maxls1 = max([l.bandwidth for l in jp1.neighs])
        maxls2 = max([l.bandwidth for l in jp2.neighs])
        maxls = max(maxls1, maxls2)

        jp1.nn.addNeigh(jp2.nn, bw=maxls)

        if removeJoinPointsUsed:
            jp1.nn.joinPoint = False
            jp2.nn.joinPoint = False

    if removeJoinPointsTopo1:
        for n in jps1:
            n.nn.joinPoint = False
    if removeJoinPointsTopo2:
        for n in jps2:
            n.nn.joinPoint = False

    return new_topo
