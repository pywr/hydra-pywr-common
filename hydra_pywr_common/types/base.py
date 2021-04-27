"""
Base types for model types
"""
from .fragments import(
    PywrGeographicPosition,
    PywrPosition
)

edge_types = []
recorder_types = []


class PywrEntity():
    """ Base type for all elements capable of
        appearing in a Pywr network
    """
    pass


class PywrNode(PywrEntity):
    node_type_map = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        PywrNode.node_type_map[cls.key] = cls

    def __init__(self, data, **kwargs):
        #print(data)
        self.name = data["name"]
        location = data.get("position")
        self.position = PywrPosition.PywrPositionFactory(location) if location else None

    @staticmethod
    def NodeFactory(data):
        instkey = data["type"]
        instcls = PywrNode.node_type_map[instkey]
        return instcls(data)


class PywrEdge(PywrEntity):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        edge_types.append(cls)


class PywrParameter(PywrEntity):
    tag = "PYWR_PARAMETER"
    parameter_type_map = {}
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        PywrParameter.parameter_type_map[cls.key] = cls

    @staticmethod
    def ParameterFactory(data):
        instkey = data["type"]
        instcls = PywrParameter.parameter_type_map[instkey]
        return instcls(data)


class PywrRecorder(PywrEntity):
    tag = "PYWR_RECORDER"
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        recorder_types.append(cls)
