import json
from pprint import pprint

from hydra_pywr_common.types.nodes import(
    PywrNode,
    PywrParameter,
    PywrCatchmentNode
)

from hydra_pywr_common.types.parameters import(
    PywrDataframeParameter
)

from hydra_pywr_common.types.recorders import(
    PywrFlowDurationCurveRecorder
)

from hydra_pywr_common.types.network import(
    PywrNetwork
)

from hydra_pywr_common.lib.writers import PywrJsonWriter, PywrHydraWriter


#from hydra_pywr_common.types import *

def _b(txt=None, width=78):
    centre = f"  {txt}  " if txt else "="
    print(f"\n{{:=^{width}}}".format(centre))


def _elem(elem, *attrs):
    print(elem)
    for a in attrs:
        nest = a.split('.')
        if len(nest) == 1:
            print(f"  {a:14} => {getattr(elem, a)}")
        elif len(nest) == 2:
            base = getattr(elem, nest[0])
            print(f"  {a:14} => {getattr(base, nest[1])}")

    _b()

if __name__ == "__main__":
    #infile, projection = "/home/paul/data/pywr/Tana.newparam.max_flow_series_with_catchment.json", "EPSG:4326"
    infile, projection = "/home/paul/data/pywr/ruthamford-historic.json", "EPSG:27700"
    #infile, projection = "/mnt/xfr/Ruthamford.Model.v1.08.Wansford.tests.April.2021.adding.Feland.Reservoir.aggregate.1.4938.NEW.json", "EPSG:27700"
    #infile, projection = "/mnt/xfr/Ruthamford.Model.v1.08.Wansford.tests.April.2021.adding.Feland.Reservoir.aggregate.json", "EPSG:27700"

    """
    with open(infile, 'r') as fp:
        src = json.load(fp)

    _b()
    ndata = src["nodes"][0] # catchment

    print(ndata)
    n = PywrNode.NodeFactory(ndata)

    _elem(n, "name", "flow", "flow.value", "position")
    #exit(55)
    #print(n.flow.dataset)

    ldata = src["nodes"][-1]    # link

    l = PywrNode.NodeFactory(ldata)
    _elem(l, "name", "position")

    odata = src["nodes"][-2]    # output

    o = PywrNode.NodeFactory(odata)
    _elem(o, "name", "cost", "position")

    mppdata = [*src["parameters"].items()][0]  # monthlyprofile

    print(mppdata)
    mpp = PywrParameter.ParameterFactory(mppdata)    # NB Pass data only
    _elem(mpp, "value")

    reservoirs = filter(lambda i: i["type"] == "reservoir", src["nodes"])

    r = PywrNode.NodeFactory([*reservoirs][0])
    _elem(r, "name", "max_volume", "bathymetry", "weather", "position")

    somenode = { "name": "Bernard",
                 "type": "sentient_carrot",
                 "colour": "orange",
                 "hasLeaves": True,
                 "length": 17.2,
                 "history": [ 0.0, 2.5, 6.0, 9.3, 14.4 ]
               }

    carrot = PywrNode.NodeFactory(somenode)
    _elem(carrot, "name", "type", "colour", "hasLeaves", "length", "history")
    """

    pnet = PywrNetwork.from_source_file(infile)

    """
    _elem(pnet, "timestepper", "metadata")
    #print(pnet.nodes)
    #print(pnet.parameters)

    output_nodes = filter(lambda n: n.key == "output", pnet.nodes.values())
    delta_cotton = [*output_nodes][0]
    _elem(delta_cotton, "name", "cost", "max_flow", "max_flow.value")
    print(type(delta_cotton.max_flow))
    print(delta_cotton.__dict__)
    print(delta_cotton.max_flow.name)
    print(delta_cotton.has_unresolved_parameter_reference)
    print(delta_cotton.unresolved_parameter_references)

    #print(pnet.recorders)
    #print(pnet.edges)
    #print(pnet.timestepper.start, pnet.timestepper.end, pnet.timestepper.timestep)
    _b()
    for attrname, attr in delta_cotton.__dict__.items():
        print(f"{attrname} => {attr}")
    print(delta_cotton.max_flow.name)
    print(delta_cotton.max_flow.value)
    print(delta_cotton.pywr_json)
    _b()
    node = [*pnet.nodes.values()][0]
    print(node.name)
    print(node.pywr_node)
    print(node.__dict__)
    #print(node.pywr_json)
    _b()
    #print(pnet.parameters)
    #writer = PywrJsonWriter(pnet)
    agg_nodes = filter(lambda n: n.key == "aggregatednode", pnet.nodes.values())
    #agg_nodes = filter(lambda n: n.name == "Ouse Washes diversion ratio", pnet.nodes.values())
    for idx, n in enumerate(agg_nodes):
        _b(f"agg_node[{idx}]")
        print(n, n.key)
        print(vars(n))
    #output = writer.as_dict()
    #with open("/tmp/ruth.json", mode='w') as fp:
    #    json.dump(output, fp, indent=2)
    """

    """
    for node in pnet.nodes.values():
        print(node.name)
        print(node.pywr_json)
        _b()
    """
    """
    hydra_json = "/mnt/xfr/Tana_river_basin_catchment_04-1.2021-05-04.16-07-51.json"

    with open(hydra_json, 'r') as fp:
        hydra_src = json.load(fp)

    hnet = PywrNetwork.from_hydra_network(hydra_src)
    """
    _b("Hydra Network")
    hwriter = PywrHydraWriter(pnet, user_id=2, template_id=1, project_id=4)
    hwriter.build_hydra_network(projection)
    #gitaru = pnet.nodes["Gitaru"]
    #print(gitaru)
    #print(vars(gitaru))
    #print(gitaru.bathymetry.value)
    #pprint(pnet.parameters)
    #exit(77)
    """
    link48 = pnet.nodes["link_48"]
    print(link48)
    print(vars(link48))
    print(link48.recorders)
    print(link48.fdc)
    """
    #uprnodes = [ n for n in pnet.nodes.values() if n.has_unresolved_parameter_reference ]
    #print(f"{uprnodes=}")
    """
    for node in pnet.nodes.values():
        print(f"{node.name} => {node.type.value}")
        if node.name == "Aggregated Demand":
            print(f"{node.unresolved_parameter_references=}")
            print(node.__dict__)
            print(node.intrinsic_attrs)
            print(node.parameters)
            print(node.recorders)
        #for attr_name in node.parameters:
        for attr_name in node.intrinsic_attrs:
            if attr_name == "type":
                continue
            print(node.attr_dataset(attr_name))
        print()
    """
