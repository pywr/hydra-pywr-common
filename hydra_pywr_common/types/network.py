import json
import logging as log
from hydra_pywr_common.lib.readers import(
    PywrJsonReader,
    PywrHydraReader
)

from hydra_pywr_common.lib.utils import parse_reference_key
from hydra_pywr_common.types.fragments.config import IntegratedConfig


class PywrNetwork():
    def __init__(self, reader):
        self.metadata = reader.metadata
        self.timestepper = reader.timestepper
        self.tables = reader.tables
        self.scenarios = reader.scenarios
        self.nodes = reader.nodes
        self.edges = reader.edges
        self.parameters = reader.parameters
        self.recorders = reader.recorders
        #This is the set of all parameters which should be written as
        #network attributes, instead of on nodes. This is indentified by virtue
        #of a parameter name not having the "__Node Name__:attr_name" format
        self.node_defined_parameters = []
        #This is the set of all recorders which should be written as
        #network attributes, instead of on nodes. This is indentified by virtue
        #of a parameter name not having the "__Node Name__:attr_name" format
        self.node_defined_recorders = []

    @classmethod
    def from_source_file(cls, infile):
        reader = PywrJsonReader(filename=infile)
        return cls(reader)

    @classmethod
    def from_source_json(cls, jsonsrc):
        reader = PywrJsonReader(jsonsrc=jsonsrc)
        return cls(reader)


    @classmethod
    def from_hydra_network(cls, hydra_net):
        reader = PywrHydraReader(hydra_net)
        return cls(reader)

    @property
    def title(self):
        return self.metadata.title.get_value()

    def resolve_parameter_references(self):
        """  Arbitrary references on nodes are created as PywrDescriptorReference.
             This function examines any such references and replaces them with an
             instance of the appropriate PywrParameter.
        """
        for node in self.nodes.values():
            refs = node.unresolved_parameter_references
            for attrname, refinst in refs:
                ##Check whether this attribute should go on the node or the network by
                #checking the naming of the parameter to see if it confroms to the
                #__node name__:attr_name format -- the 'reference key'
                try:
                    node_name, attr_name = parse_reference_key(refinst.get_value())
                    self.node_defined_parameters.append(refinst.get_value())
                except (ValueError, IndexError) as e:
                    continue

                try:
                    param = self.parameters[refinst.name]
                    setattr(node, attrname, param)
                    log.info(f"parameter attr to parameter: {node.name} => a: {attrname} ri.n: {refinst.name}")
                except KeyError as e:
                    try:
                        param = self.parameters[refinst.get_value()]
                        setattr(node, attrname, param)
                        log.info(f"descriptor attr to parameter: {node.name} => a: {attrname} ri.v: {refinst.get_value()}")
                    except KeyError as e:
                        pass    # Remains as descriptor reference
                        log.info(f"plain descriptor: {node.name} => a: {attrname} ri.v: {refinst.get_value()}")


    def resolve_recorder_references(self):
        """  Arbitrary references on nodes are created as PywrDescriptorReference.
             This function examines any such references and replaces them with an
             instance of the appropriate PywrRecorder.
        """
        for node in self.nodes.values():
            refs = node.unresolved_parameter_references
            for attrname, refinst in refs:

                ##Check whether this attribute should go on the node or the network by
                #checking the naming of the parameter to see if it confroms to the
                #__node name__:attr_name format -- the 'reference key'
                try:
                    node_name, attr_name = parse_reference_key(refinst.get_value())
                    self.node_defined_recorders.append(refinst.get_value())
                except (ValueError, IndexError) as e:
                    continue


                try:
                    rec = self.recorders[refinst.name]
                    setattr(node, attrname, rec)
                    log.info(f"recorder attr to recorder: {node.name} => a: {attrname} ri.n: {refinst.name}")
                except KeyError as e:
                    try:
                        param = self.recorders[refinst.get_value()]
                        setattr(node, attrname, param)
                        log.info(f"descriptor attr to recorder: {node.name} => a: {attrname} ri.v: {refinst.value}")
                    except KeyError as e:
                        pass    # Remains as descriptor reference
                        log.info(f"plain descriptor: {node.name} => a: {attrname} ri.v: {refinst.get_value()}")


    def resolve_backwards_recorder_references(self):
        """  A Pywr network definition contains a collection of the recorders it defines, each
             of which may contain a 'backwards' reference to the node on which it is present.
             This may be the only connection between the node and its recorder, as it is not
             required that the node contain a 'forward' reference to any recorders.
             This function examines the recorders collection, and adds a forward reference to
             each node which is the target of a backwards reference.
        """
        for noderef, rec in self.recorders.items():
            nodename, attrname = parse_reference_key(noderef)
            try:
                node = self.nodes[nodename]
            except KeyError as e:
                raise
            setattr(node, attrname, rec)
            log.info(f"recorder added: {node.name} => a: {attrname}")
            if attrname not in node.intrinsic_attrs:
                node.intrinsic_attrs.append(attrname)


    def resolve_backwards_recorder_references_by_node_key(self):
        """  As resolve_backwards_recorder_references, but uses an internal .node
             attr on each recorder rather than the recorder's key in the collection.
        """
        for rec in self.recorders.values():
            try:
                node = rec["node"]
            except KeyError:
                pass
            setattr(node, attrname, rec)
            if attrname not in node.intrinsic_attrs:
                node.intrinsic_attrs.append(attrname)


    def resolve_backwards_parameter_references(self):
        """  A Pywr network definition contains a collection of the parameters it defines, each
             of which may contain a 'backwards' reference to the node on which it is present.
             This may be the only connection between the node and its parameter, as it is not
             required that the node contain a 'forward' reference to any parameter.
             This function examines the parameters collection, and adds a forward reference to
             each node which is the target of a backwards reference.
        """
        for noderef, param in self.parameters.items():
            nodename, attrname = parse_reference_key(noderef)
            try:
                node = self.nodes[nodename]
            except KeyError as e:
                continue
            setattr(node, attrname, param)
            if attrname not in node.intrinsic_attrs:
                node.intrinsic_attrs.append(attrname)
            log.info(f"Added param <{param.key}> to {node.name} as {attrname}")


    def speculative_forward_references(self):
        """  Forward references on a node to the parameters or recorders it contains
             are not required to adhere to the canonical __node__:attr format for
             references, and practical examples may take various forms such as
             "node_attr" or "node attr" which leads to similarities between reference
             names and the names of parameters or recorders.
             This function applies some heuristics to such references which attempt
             to determine the intended target of a reference.
        """
        import re
        from string import whitespace
        # Reverse order to avoid mutating container
        nodes = reversed(sorted(self.nodes.values(), key=len))
        seen = set()

        for node in nodes:
            tr_tab = { ord(c): '.' for c in whitespace }
            p = re.compile(node.name.translate(tr_tab)+"_")
            node_refs = {}
            references = {**self.parameters, **self.recorders}

            for k,v in references.items():
                # NB Python 3.8+
                if m := p.match(k):
                    if v in seen:
                        continue
                    node_refs[k[m.end():]] = v
                    seen.add(v)

            for attr, ref in node_refs.items():
                setattr(node, attr, ref)
                log.info(f"[sfr] {node.name} a: {attr} => {ref}")
                if attr not in node.intrinsic_attrs:
                    node.intrinsic_attrs.append(attr)


"""
    Integrated Network
"""


class PywrIntegratedNetwork():
    def __init__(self, water, energy, config):
        self.water = water
        self.energy = energy
        self.config = config


    @classmethod
    def from_combined_file(cls, filename):
        with open(filename, 'r') as fp:
            src = json.load(fp)

        water_src = src["water_network"]
        water = PywrNetwork.from_source_json(water_src)

        energy_src = src["energy_network"]
        energy = PywrNetwork.from_source_json(energy_src)

        config_src = src["config"]
        config = IntegratedConfig(config_src)

        return cls(water, energy, config)


    @classmethod
    def from_instances(cls, water, energy, config):
        return cls(water, energy, config)


    @property
    def domains(self):
        return ("water", "energy")
