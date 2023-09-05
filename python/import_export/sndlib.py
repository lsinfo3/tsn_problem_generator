from lib.topology import Topology


def from_sndlib(sndlib_native_format: str) -> Topology:
    topo = Topology()

    for l in sndlib_native_format.split("\n"):
        pass

    # TODO

    return topo