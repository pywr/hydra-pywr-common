from hydra_pywr_common.types.base import(
    PywrNode,
    PywrParameter,
    PywrRecorder,
    PywrEdge
)

from hydra_pywr_common.lib.utils import(
    parse_reference_key
)

from hydra_pywr_common.lib.readers import(
    PywrJsonReader,
    PywrHydraReader
)

from .fragments.network import(
    Timestepper,
    Metadata
)


class PywrNetwork():

    def __init__(self, reader):
        self.metadata = reader.metadata
        self.timestepper = reader.timestepper
        self.nodes = reader.nodes
        self.edges = reader.edges
        self.parameters = reader.parameters
        self.recorders = reader.recorders

        #self.resolve_parameter_references()
        #self.resolve_recorder_references()


    @classmethod
    def from_source_file(cls, infile):
        reader = PywrJsonReader(infile)
        return cls(reader)


    @classmethod
    def from_hydra_network(cls, hydra_net):
        reader = PywrHydraReader(hydra_net)
        return cls(reader)


    def resolve_parameter_references(self):
        for node in self.nodes.values():
            refs = node.unresolved_parameter_references
            for attrname, refinst in refs:
                try:
                    param = self.parameters[refinst.name]
                except KeyError as e:
                    # No such param
                    raise
                print(attrname)
                #nodename, nodeattr = parse_reference_key(attrname)
                #setattr(node, attr, param)
                setattr(node, attrname, param)


    def resolve_recorder_references(self):
        for noderef, rec in self.recorders.items():
            nodename, attrname = parse_reference_key(noderef)
            try:
                node = self.nodes[nodename]
            except KeyError as e:
                # No such node
                raise
            setattr(node, attrname, rec)
