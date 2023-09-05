from lib.topology import Topology


def from_graphml(graphml_format: str) -> Topology:
    topo = Topology()

    for l in graphml_format.split("\n"):
        pass

    # TODO

    return topo


def to_graphml(topo: Topology, path: str):
    pass
