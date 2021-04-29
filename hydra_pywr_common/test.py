import json

from hydra_pywr_common.types.model import(
    PywrNode,
    PywrParameter
)

from hydra_pywr_common.types.model import(
    PywrCatchmentNode
)

from hydra_pywr_common.types.parameters import(
    PywrDataframeParameter
)

from hydra_pywr_common.types.network import(
    PywrNetwork
)

from hydra_pywr_common.types import *

def _b():
    print('='*16)

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
    infile = "/home/paul/data/pywr/Tana.newparam.max_flow_series_with_catchment.json"

    with open(infile, 'r') as fp:
        src = json.load(fp)

    _b()
    ndata = src["nodes"][0] # catchment

    n = PywrNode.NodeFactory(ndata)

    _elem(n, "name", "flow", "flow.value", "position")
    #print(n.flow.dataset)

    ldata = src["nodes"][-1]    # link

    l = PywrNode.NodeFactory(ldata)
    _elem(l, "name", "position")

    odata = src["nodes"][-2]    # output

    o = PywrNode.NodeFactory(odata)
    _elem(o, "name", "cost", "position")

    mppdata = [*src["parameters"].items()][0]  # monthlyprofile

    print(mppdata)
    mpp = PywrParameter.ParameterFactory(mppdata[1])    # NB Pass data only
    _elem(mpp, "value")

    reservoirs = filter(lambda i: i["type"] == "reservoir", src["nodes"])

    r = PywrNode.NodeFactory([*reservoirs][0])
    _elem(r, "name", "max_volume", "bathymetry", "weather", "position")

    """
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

    _elem(pnet, "timestepper", "metadata")
    print(pnet.nodes)
