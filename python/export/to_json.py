import json
from json import JSONEncoder
from pathlib import Path

from lib.stream import Stream
from lib.topology import Topology, Node, Link


def to_json(topo: Topology, path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as file:
        json.dump(topo.to_json_dict(), file, indent=4, cls=MyEncoder)


class MyEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Node):
            return o.to_json_dict()
        if isinstance(o, Link):
            return o.to_json_dict()
        if isinstance(o, Stream):
            return o.to_json_dict()
        return JSONEncoder.default(self, o)


