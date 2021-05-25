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
    Metadata,
    Table
)


class PywrNetwork():

    def __init__(self, reader):
        self.metadata = reader.metadata
        self.timestepper = reader.timestepper
        self.tables = reader.tables
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
                    setattr(node, attrname, param)
                    #print(f"parameter attr to parameter: {node.name} => a: {attrname} ri.n: {refinst.name}")
                except KeyError as e:
                    try:
                        param = self.parameters[refinst.value]
                        setattr(node, attrname, param)
                        #print(f"descriptor attr to parameter: {node.name} => a: {attrname} ri.v: {refinst.value}")
                    except KeyError as e:
                        #print(f"plain descriptor: {node.name} => a: {attrname} ri.v: {refinst.value}")
                        pass


    def resolve_recorder_references(self):
        for node in self.nodes.values():
            refs = node.unresolved_parameter_references
            for attrname, refinst in refs:
                try:
                    rec = self.recorders[refinst.name]
                    setattr(node, attrname, rec)
                    print(f"recorder attr to recorder: {node.name} => a: {attrname} ri.n: {refinst.name}")
                except KeyError as e:
                    try:
                        param = self.recorders[refinst.value]
                        setattr(node, attrname, param)
                        print(f"descriptor attr to recorder: {node.name} => a: {attrname} ri.v: {refinst.value}")
                    except KeyError as e:
                        print(f"plain descriptor: {node.name} => a: {attrname} ri.v: {refinst.value}")


    def resolve_backwards_recorder_references(self):
        for noderef, rec in self.recorders.items():
            nodename, attrname = parse_reference_key(noderef)
            try:
                node = self.nodes[nodename]
            except KeyError as e:
                raise
            setattr(node, attrname, rec)
            print(f"recorder added: {node.name} => a: {attrname}")
            if attrname not in node.intrinsic_attrs:
                node.intrinsic_attrs.append(attrname)


    def resolve_backwards_parameter_references(self):
        for noderef, param in self.parameters.items():
            nodename, attrname = parse_reference_key(noderef)
            try:
                node = self.nodes[nodename]
            except KeyError as e:
                raise
            setattr(node, attrname, param)
            if attrname not in node.intrinsic_attrs:
                node.intrinsic_attrs.append(attrname)
            print(f"Added param <{param.key}> to {node.name} as {attrname}")


    def speculative_forward_references(self):
        import re
        from string import whitespace
        nodes = reversed(sorted(self.nodes.values(), key=len))
        seen = set()

        for node in nodes:
            tr_tab = { ord(c): '.' for c in whitespace }
            p = re.compile(node.name.translate(tr_tab))
            node_refs = {}
            references = {**self.parameters, **self.recorders}

            for k,v in references.items():
                if m := p.match(k):
                    if v in seen:
                        continue
                    node_refs[k[m.end()+1:]] = v
                    seen.add(v)

            for attr, ref in node_refs.items():
                setattr(node, attr, ref)
                print(f"[sfr] {node.name} a: {attr} => {ref}")
                if attr not in node.intrinsic_attrs:
                    node.intrinsic_attrs.append(attr)

