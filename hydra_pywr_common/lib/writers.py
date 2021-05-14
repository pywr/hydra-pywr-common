import json

from hydra_pywr_common.types.base import(
    PywrNode,
    PywrParameter,
    PywrRecorder,
    PywrEdge
)

from hydra_pywr_common.lib.utils import(
    parse_reference_key
)

from hydra_pywr_common.types.fragments.network import(
    Timestepper,
    Metadata
)

from hydra_pywr_common.types.network import PywrNetwork


"""
    PywrNetwork => Pywr_json
"""
class PywrJsonWriter():

    def __init__(self, network):
        self.network = network

    def as_dict(self):
        output = {}

        output["timestepper"] = self.process_timestepper()
        output["metadata"] = self.process_metadata()
        output["parameters"] = self.process_parameters()
        output["recorders"] = self.process_recorders()
        output["nodes"] = self.process_nodes()
        output["edges"] = self.process_edges()

        return output

    def as_json(self, **json_opts):
        output = self.as_dict()
        return json.dumps(output, **json_opts)


    def process_timestepper(self):
        timestepper = self.network.timestepper
        return { "start": timestepper.start,
                 "end": timestepper.end,
                 "timestep": timestepper.timestep
               }

    def process_metadata(self):
        metadata = self.network.metadata
        return { "title": metadata.title,
                 "description": metadata.description
               }

    def process_parameters(self):
        parameters = self.network.parameters

        return { ref: param.value for ref, param in parameters.items() }

    def process_recorders(self):
        recorders = self.network.recorders

        return { ref: rec.value for ref, rec in recorders.items() }

    def process_nodes(self):
        nodes = self.network.nodes

        return [ node.pywr_node for node in nodes.values() ]

    def process_edges(self):
        edges = self.network.edges
        return [ edge.value for edge in edges.values() ]



def make_hydra_attr(name, desc=None):
    return { "name": name,
             "description": desc if desc else name
           }

"""
    PywrNetwork => Hydra_network
"""
class PywrHydraWriter():
    def __init__(self, network):
        self.network = network

    def initialise_hydra_connection(self,
                                    hostname=None,
                                    session_id=None,
                                    user_id=None,
                                    template_name=None,
                                    project_id=None):
        from hydra_client.connection import JSONConnection
        self.hydra = JSONConnection(hostname, session_id=session_id, user_id=user_id)
        self.project_id = project_id

        print(f"Retrieving template '{template_name}'...")
        self.template = self.hydra.get_template_by_name(template_name)


    def build_hydra_network(self):

        """ Register Hydra attributes """
        self.hydra_attributes = self.register_hydra_attributes()

        """ Build network elements and resource_scenarios with datasets """

        """ Create baseline scenario with resource_scenarios """

        """ Assemble complete network """

        """ Pass network to Hydra"""
        self.initialise_hydra_connection(user_id=2, template_name="Pywr Full template (Jan2021)")


    def register_hydra_attributes(self):
        local_attrs = {}

        for node in self.network.nodes.values():
            for attr_name in vars(node):
                if attr_name in local_attrs:
                    continue
                attr = make_hydra_attr(attr_name)
                local_attrs[attr["name"]] = attr

        print(local_attrs)
        """ Add attributes for parameter attr names"""

        return [*local_attrs.values()]
