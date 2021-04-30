import json

from hydra_pywr_common.types.base import(
    PywrNode,
    PywrParameter
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

        self.parameters = self.build_parameters()
        self.nodes = self.build_nodes()
        self.resolve_parameter_references()

        return self


    def build_nodes(self):
        nodes = {}
        for node in self.src["nodes"]:
            n = PywrNode.NodeFactory(node)
            nodes[n.name] = n

        return nodes


    def build_parameters(self):
        parameters = {}
        src_params = self.src.get("parameters")
        if src_params:
            for param in src_params.items():
                p = PywrParameter.ParameterFactory(param)
                parameters[p.name] = p

        return parameters


    def resolve_parameter_references(self):
        for node in self.nodes.values():
            refs = node.unresolved_parameter_references
            for attrname, refinst in refs:
                try:
                    param = self.parameters[refinst.name]
                except KeyError as e:
                    # No such param
                    raise
                setattr(node, attrname, param)
