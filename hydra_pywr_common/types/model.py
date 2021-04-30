from .base import(
    PywrNode,
    PywrEdge,
    PywrParameter,
    PywrRecorder,
    PywrDataReference
)

from .fragments.misc import(
    PywrBathymetry,
    PywrWeather
)

from .fragments.position import(
    PywrPosition
)

class PywrCatchmentNode(PywrNode):
    key = "catchment"

    def __init__(self, data):
        super().__init__(data)

        #self.flow = PywrParameter.ParameterFactory(data["flow"])

        #rand_data = data["flow"]    # A dataframeparameter
        #rand_data = "Some text"
        #rand_data = [ 1,2,3,4,5,6,7,8,9 ]
        #rand_data = 1.23
        self.flow = PywrDataReference.ReferenceFactory("flow", data["flow"])


class PywrLinkNode(PywrNode):
    key = "link"

    def __init__(self, data):
        super().__init__(data)


class PywrOutputNode(PywrNode):
    key = "output"

    def __init__(self, data):
        super().__init__(data)

        self.cost = data.get("cost", 0)

        # Add max_flow parameter reference
        max_flow = data.get("max_flow")
        self.max_flow = PywrDataReference.ReferenceFactory("max_flow", max_flow) if max_flow else 0


"""
class PywrReservoir(PywrNode):
    key = "reservoir"

    def __init__(self, data):
        super().__init__(data)

        self.max_volume = data["max_volume"]
        self.initial_volume = data["initial_volume"]
        self.bathymetry = PywrBathymetry(data["bathymetry"])
        self.weather = PywrWeather(data["weather"])
"""

class PywrLinearStorageReleaseControlNode(PywrNode):
    key = "linearstoragereleasecontrol"

    def __init__(self, data):
        super().__init__(data)

        self.release_values = PywrDataReference.ReferenceFactory("release_values", data["release_values"])
        self.storage_node = PywrDataReference.ReferenceFactory("storage_node", data["storage_node"])


class PywrRiverGaugeNode(PywrNode):
    key = "rivergauge"

    def __init__(self, data):
        super().__init__(data)

        self.cost = PywrDataReference.ReferenceFactory("cost", data["cost"])


class PywrCustomNode(PywrNode):
    key = "__custom_node__"

    def __init__(self, data):
        super().__init__(data)
        #print(data)
        self.intrinsic_attrs = []
        self.parse_data(data)

    def parse_data(self, data):
        for attr, value in data.items():
            if attr in PywrNode.base_attrs:
                continue

            typed_attr = PywrDataReference.ReferenceFactory(attr, value)
            setattr(self, attr, typed_attr)
            self.intrinsic_attrs.append(attr)
