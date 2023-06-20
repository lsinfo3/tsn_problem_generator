import math
import random
from typing import Union, Tuple, List

from lib.stream import Stream
from lib.topology import Topology

MyRangeType = Union[int, float, List, Tuple]

def create_streams_for_topology(topo: Topology, num_streams: int, burst_range: MyRangeType, rate_range: MyRangeType, prio_range: MyRangeType, min_pathlen: int = 1, max_pathlen: int = None) -> List[Stream]:
    devices = topo.hosts
    counter = len(topo.get_all_streams())
    streams = []
    printed_warnings = 0

    for i in range(num_streams):
        n1 = None
        n2 = None

        if min_pathlen <= 1 and max_pathlen == None:
            n1, n2 = random.sample(devices, 2)
        else:
            if max_pathlen == None: max_pathlen = len(topo.nodes)
            n1, = random.sample(devices, 1)
            n2_choices = []
            for j in range(100):
                if len(n2_choices) > 0: break
                n1, = random.sample(devices, 1)
                n2_choices = [n for n in topo.get_other_devices_within_distance(n1, min_pathlen, max_pathlen) if n.type == "host"]

            if len(n2_choices) == 0:
                printed_warnings += 1
                if printed_warnings == 5:
                    print(f"Further warnings suppressed...")
                elif printed_warnings < 5:
                    print(f"Warning: no suitable pairs with {min_pathlen=}, {max_pathlen=}")
            else:
                n2, = random.sample(n2_choices, 1)

        def unpack_random(varrange):
            if type(varrange) in (tuple, list):
                if len(varrange) < 2 or len(varrange) > 3:
                    raise ValueError("range can either be a number, or a list [min, max], or a list [min, max, 'log']")
                elif len(varrange) == 3 and varrange[2] == "log":
                    return exprandom_float_between(varrange[0], varrange[1])
                elif len(varrange) == 3:
                    raise ValueError("range[2] can only be 'log' for logarithmically scaled random choice")
                else:
                    return urandom_int_between(varrange[0], varrange[1])
            return varrange

        if n2:
            burst = unpack_random(burst_range)
            rate = unpack_random(rate_range)
            prio = unpack_random(prio_range)

            stream = Stream(label = f"st{counter+i}",
                            path = topo.shortest_path(n1, n2),
                            priority = prio,
                            rate = rate,
                            burst = burst,
                            minFrameSize = 64*8,
                            maxFrameSize = min(burst-20*8, 1500*8))
            streams.append(stream)

    return streams


def urandom_int_between(min: int, max: int) -> int:
    return random.choice(range(min, max+1))

def urandom_float_between(min: float, max: float) -> float:
    return random.random() * (max - min) + min

def exprandom_float_between(min: float, max: float) -> float:
    return math.exp(urandom_float_between(math.log(min), math.log(max)))
