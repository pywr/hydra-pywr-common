import json

from hydra_pywr_common.types.base import(
    PywrNode,
    PywrParameter,
    PywrRecorder,
    PywrEdge
)

from hydra_pywr_common.types.fragments.network import(
    Timestepper,
    Metadata,
    Table,
    Scenario
)

class PywrJsonReader():

    def __init__(self, filename=None, jsonsrc=None):

        if filename is not None:
            with open(filename, 'r') as fp:
                self.src = json.load(fp)
        else:
            self.src = jsonsrc

        self.build_network_from_json()


    def build_network_from_json(self):
        self.timestepper = Timestepper(self.src["timestepper"])
        self.metadata = Metadata(self.src["metadata"])
        self.tables = self.build_tables()
        self.scenarios = self.build_scenarios()

        self.parameters = self.build_parameters()
        self.recorders = self.build_recorders()
        self.nodes = self.build_nodes()
        self.edges = self.build_edges()


    def build_nodes(self):
        nodes = {}
        for node in self.src["nodes"]:
            n = PywrNode.NodeFactory(node)
            nodes[n.name] = n

        return nodes

    def build_edges(self):
        edges = {}
        for edge in self.src["edges"]:
            e = PywrEdge(edge)
            edges[e.name] = e

        return edges


    def build_parameters(self):
        parameters = {}
        src_params = self.src.get("parameters")
        if src_params:
            for param in src_params.items():
                p = PywrParameter.ParameterFactory(param)
                parameters[p.name] = p

        return parameters


    def build_recorders(self):
        recorders = {}
        src_recorders = self.src.get("recorders")
        if src_recorders:
            for recorder in src_recorders.items():
                r = PywrRecorder.RecorderFactory(recorder)
                recorders[r.name] = r

        return recorders

    def build_tables(self):
        tables = {}
        src_tables = self.src.get("tables")
        if src_tables:
            for name, table in src_tables.items():
                t = Table(table)
                tables[name] = t

        return tables

    def build_scenarios(self):
        scenarios = {}
        src_scenarios = self.src.get("scenarios", [])
        for scen in src_scenarios:  # list of dicts
            s = Scenario(scen)
            scenarios[s.name.value] = s

        return scenarios



class PywrHydraReader():
    def __init__(self, hydra_net):
        self.metadata = None
        self.timestepper = None
        self.parameters = {}
        self.recorders = {}
        self.nodes = {}
        self.edges = {}
