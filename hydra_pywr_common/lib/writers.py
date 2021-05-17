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

    default_map_projection = "EPSG:4326"

    def __init__(self, network):
        self.network = network

        self._next_node_id = 0
        self._next_link_id = 0
        self._next_attr_id = 0


    def get_typeid_by_name(self, name):
        for t in self.template["templatetypes"]:
            if t["name"] == name:
                return t["id"]

    def get_hydra_network_type(self):
        for t in self.template["templatetypes"]:
            if t["resource_type"] == "NETWORK":
                return t

    def get_hydra_attrid_by_name(self, attr_name):
        for attr in self.hydra_attributes:
            if attr["name"] == attr_name:
                return attr["id"]

    def get_next_node_id(self):
        self._next_node_id -= 1
        return self._next_node_id

    def get_next_link_id(self):
        self._next_link_id -= 1
        return self._next_link_id

    def get_next_attr_id(self):
        self._next_attr_id -= 1
        return self._next_attr_id

    def make_baseline_scenario(self, resource_scenarios):
        return { "name": "Baseline",
                 "description": "hydra-pywr Baseline scenario",
                 "resourcescenarios": resource_scenarios if resource_scenarios else []
               }


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

        self.initialise_hydra_connection(user_id=2, template_name="Pywr Full template (Jan2021)")
        """ Register Hydra attributes """
        self.hydra_attributes = self.register_hydra_attributes()
        print(self.hydra_attributes)

        self.network.resolve_parameter_references()
        self.network.resolve_recorder_references()

        """ Build network elements and resource_scenarios with datasets """
        self.hydra_nodes, node_scenarios = self.build_hydra_nodes()
        print(self.hydra_nodes)
        print(node_scenarios)
        self.network_attributes, network_scenarios = self.build_network_attributes()
        print(self.network_attributes)
        print(network_scenarios)

        resource_scenarios = node_scenarios + network_scenarios # + link_scenarios

        """ Create baseline scenario with resource_scenarios """
        baseline_scenario = make_baseline_scenario(resource_scenarios)

        """ Assemble complete network """
        network_name = self.network.metadata.title
        network_hydratype = self.get_hydra_network_type()
        network_description = self.network.metadata.description
        map_projection = self.metadata.projection if self.metadata.projection else PywrHydraWriter.default_map_projection

        hydra_network = {
            "name": network.name,
            "description": network_description,
            "project_id": self.project_id,
            "nodes": self.hydra_nodes,
            "layout": None,
            "scenarios": [baseline_scenario],
            "projection": map_projection,
            "attributes": self.network_attributes,
            "types": [{ "id": network_hydratype["id"] }]
        }

        """ Pass network to Hydra"""


    def register_hydra_attributes(self):
        #pending_attrs = set(attr_name for attr_name in PywrNode.base_attrs)
        timestepper_attrs = { 'timestepper.start', 'timestepper.end', 'timestepper.timestep'}
        excluded_attrs = { 'position', 'intrinsic_attrs', 'type' }
        pending_attrs = timestepper_attrs

        for node in self.network.nodes.values():
            #for attr_name in vars(node):
            for attr_name in node.intrinsic_attrs:
                pending_attrs.add(attr_name)

        attrs = [ make_hydra_attr(attr_name) for attr_name in pending_attrs - excluded_attrs ]

        #print(attrs)
        return self.hydra.add_attributes(attrs)


    def make_resource_attr_and_scenario(self, element, attr_name, datatype=None):
        local_attr_id = self.get_next_attr_id()
        resource_scenario = self.make_resource_scenario(element, attr_name, local_attr_id, datatype)
        resource_attribute = { "id": local_attr_id,
                               "attr_id": self.get_hydra_attrid_by_name(attr_name),
                               "attr_is_var": "N"
                             }

        return resource_attribute, resource_scenario


    def make_resource_scenario(self, element, attr_name, local_attr_id, datatype=None):
        dataset = element.attr_dataset(attr_name)

        resource_scenario = { "resource_attr_id": local_attr_id,
                              "dataset": dataset
                            }

        return resource_scenario


    def build_hydra_nodes(self):
        hydra_nodes = []
        resource_scenarios = []

        exclude_node_attrs = ('type',)

        for node in self.network.nodes.values():
            resource_attributes = []

            # TODO Fix this is node ctor path
            for attr_name in filter(lambda a: a not in exclude_node_attrs, node.intrinsic_attrs):
                ra, rs = self.make_resource_attr_and_scenario(node, attr_name)
                resource_attributes.append(ra)
                resource_scenarios.append(rs)

            hydra_node = {}
            hydra_node["resource_type"] = "NODE"
            hydra_node["id"] = self.get_next_node_id()
            hydra_node["name"] = node.name
            hydra_node["layout"] = {}
            hydra_node["attributes"] = resource_attributes
            hydra_node["types"] = [{ "id": self.get_typeid_by_name(node.key) }]

            if hasattr(node, "position"):
                hydra_node["x"] = node.position.long
                hydra_node["y"] = node.position.lat

            hydra_nodes.append(hydra_node)

        return hydra_nodes, resource_scenarios


    def build_network_attributes(self):
        hydra_network_attrs = []
        resource_scenarios = []

        timestepper_attrs = { 'timestepper.start', 'timestepper.end', 'timestepper.timestep'}

        for attr_name in timestepper_attrs:
            ra, rs = self.make_resource_attr_and_scenario(self.network.timestepper, attr_name)
            hydra_network_attrs.append(ra)
            resource_scenarios.append(rs)

        return hydra_network_attrs, resource_scenarios