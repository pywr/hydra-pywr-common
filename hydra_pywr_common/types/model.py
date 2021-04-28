from .base import(
    PywrNode,
    PywrEdge,
    PywrParameter,
    PywrRecorder,
    PywrDataReference
)

from .fragments import(
    PywrBathymetry,
    PywrWeather
)

class PywrCatchmentNode(PywrNode):
    key = "catchment"

    def __init__(self, data):
        super().__init__(data)

        self.flow = PywrParameter.ParameterFactory(data["flow"])

        #rand_data = data["flow"]    # A dataframeparameter
        #rand_data = "Some text"
        #rand_data = [ 1,2,3,4,5,6,7,8,9 ]
        #rand_data = 1.23
        #self.flow = PywrDataReference.ReferenceFactory("flow", rand_data)


class PywrLinkNode(PywrNode):
    key = "link"

    def __init__(self, data):
        super().__init__(data)


class PywrOutputNode(PywrNode):
    key = "output"

    def __init__(self, data):
        super().__init__(data)

        self.cost = data["cost"]

        # Add max_flow parameter reference


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


class PywrCustomNode(PywrNode):
    key = "__custom_node__"

    def __init__(self, data):
        super().__init__(data)
        print(data)
        self.parse_data(data)

    def parse_data(self, data):
        for attr, value in data.items():
            if attr in PywrNode.base_attrs:
                continue

            typed_attr = PywrDataReference.ReferenceFactory(attr, value)
            setattr(self, attr, typed_attr)
