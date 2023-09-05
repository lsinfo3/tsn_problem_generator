import random
from typing import Union, Tuple, List, Set

from lib.stream import Stream
from lib.topology import Topology
from lib.y_random_util import urandom_float_between, unpack_random

MyRangeType = Union[int, float, List, Tuple, Set]


def create_streams_for_topology(topo: Topology, num_streams: int, burst_range: MyRangeType, rate_range: MyRangeType, prio_range: MyRangeType, min_pathlen: int = 1, max_pathlen: int = None, only_switch_controller_paths: bool = False) -> List[Stream]:
    counter = len(topo.get_all_streams())
    streams = []
    printed_warnings = 0

    for i in range(num_streams):
        n1 = None
        n2 = None

        if only_switch_controller_paths:
            controllers = topo.controllers
            sensors = topo.sensors

            if len(controllers) == 0 or len(sensors) == 0:
                raise ValueError(f"No controllers or no sensors found in the topology; {len(controllers)=}, {len(sensors)=}")

            if min_pathlen <= 1 and max_pathlen == None:
                n1, = random.sample(controllers, 1)
                n2, = random.sample(sensors, 1)
            else:
                if max_pathlen == None: max_pathlen = len(topo.nodes)
                n1, = random.sample(controllers, 1)
                n2_choices = []
                for j in range(100):
                    if len(n2_choices) > 0: break
                    n1, = random.sample(controllers, 1)
                    n2_choices = [n for n in topo.get_other_devices_within_distance(n1, min_pathlen, max_pathlen) if n.type == "sensor"]

                if len(n2_choices) == 0:
                    printed_warnings += 1
                    if printed_warnings == 5:
                        print(f"  Further warnings suppressed...")
                    elif printed_warnings < 5:
                        print(f"  Warning: no suitable pairs with {min_pathlen=}, {max_pathlen=}")
                else:
                    n2, = random.sample(n2_choices, 1)

            # Flip a coin to select "controller->sensor" or "sensor->controller" direction
            if urandom_float_between(0, 1) <= 0.5:
                n1, n2 = n2, n1

        else:
            devices = topo.hosts

            if min_pathlen <= 1 and max_pathlen == None:
                n1, n2 = random.sample(devices, 2)
            else:
                if max_pathlen == None: max_pathlen = len(topo.nodes)
                n1, = random.sample(devices, 1)
                n2_choices = []
                for j in range(100):
                    if len(n2_choices) > 0: break
                    n1, = random.sample(devices, 1)
                    n2_choices = [n for n in topo.get_other_devices_within_distance(n1, min_pathlen, max_pathlen) if n.is_host]

                if len(n2_choices) == 0:
                    printed_warnings += 1
                    if printed_warnings == 5:
                        print(f"  Further warnings suppressed...")
                    elif printed_warnings < 5:
                        print(f"  Warning: no suitable pairs with {min_pathlen=}, {max_pathlen=}")
                else:
                    n2, = random.sample(n2_choices, 1)

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

