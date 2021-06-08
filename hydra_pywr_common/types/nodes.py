from .base import(
    PywrNode,
    PywrDataReference
)

class PywrCatchmentNode(PywrNode):
    key = "catchment"

    def __init__(self, data):
        super().__init__(data)


class PywrLinkNode(PywrNode):
    key = "link"

    def __init__(self, data):
        super().__init__(data)


class PywrPiecewiseLinkNode(PywrNode):
    key = "piecewiselink"

    def __init__(self, data):
        super().__init__(data)


class PywrInputNode(PywrNode):
    key = "input"

    def __init__(self, data):
        super().__init__(data)


class PywrStorageNode(PywrNode):
    key = "storage"

    def __init__(self, data):
        super().__init__(data)


class PywrOutputNode(PywrNode):
    key = "output"

    def __init__(self, data):
        super().__init__(data)


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


class PywrRiverSplitWithGaugeNode(PywrNode):
    key = "riversplitwithgauge"

    def __init__(self, data):
        super().__init__(data)


class PywrRiverSplitNode(PywrNode):
    key = "riversplit"

    def __init__(self, data):
        super().__init__(data)


class PywrAggregatedNode(PywrNode):
    key = "aggregatednode"

    def __init__(self, data):
        super().__init__(data)


class PywrAggregatedStorageNode(PywrNode):
    key = "aggregatedstorage"

    def __init__(self, data):
        super().__init__(data)


class PywrAnnualVirtualStorageNode(PywrNode):
    key = "annualvirtualstorage"

    def __init__(self, data):
        super().__init__(data)


class PywrReservoirNode(PywrNode):
    key = "reservoir"

    def __init__(self, data):
        super().__init__(data)


class PywrTurbineNode(PywrNode):
    key = "turbine"

    def __init__(self, data):
        super().__init__(data)


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
