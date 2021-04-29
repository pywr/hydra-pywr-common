import json

from hydra_pywr_common.types.base import(
    PywrNode
)

from .fragments.network import(
    Timestepper,
    Metadata
)


class PywrJsonReader():
    pass

class PywrNetwork():

    def __init__(self, jsonsrc=None, hydra_network=None):
        self.src = jsonsrc
        self.nodes = None
        self.edges = None
        self.parameters = None
        self.recorders = None


    @classmethod
    def from_source_file(cls, infile):
        with open(infile, 'r') as fp:
            src = json.load(fp)

        return cls(jsonsrc=src).build_network_from_json()


    @classmethod
    def from_hydra_network(cls, hydra_net):
        pass


    def build_network_from_json(self):
        self.timestepper = Timestepper(self.src["timestepper"])
        self.metadata = Metadata(self.src["metadata"])

        self.nodes = self.build_nodes()

        return self


    def build_nodes(self):

        nodes = {}

        for node in self.src["nodes"]:
            n = PywrNode.NodeFactory(node)
            nodes[n.name] = n

        return nodes
