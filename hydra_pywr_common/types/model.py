from .base import(
    PywrNode,
    PywrEdge,
    PywrParameter,
    PywrRecorder
)

class PywrCatchmentNode(PywrNode):
    key = "catchment"

    def __init__(self, data):
        super().__init__(data)

        self.flow = PywrParameter.ParameterFactory(data["flow"])


class PywrLinkNode(PywrNode):
    key = "link"

    def __init__(self, data):
        super().__init__(data)


class PywrOutputNode(PywrNode):
    key = "output"

    def __init__(self, data):
        super().__init__(data)

        self.cost = data["cost"]
