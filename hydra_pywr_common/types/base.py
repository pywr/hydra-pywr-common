"""
Base types for model types
"""

import json
import numbers
from abc import ABC, abstractmethod

from lib.utils import(
    parse_reference_key
)

from .fragments.position import(
    PywrPosition
)


class PywrEntity():
    """ Base type for all elements capable of
        appearing in a Pywr network
    """
    pass

class HydraDataset():

    @property
    def dataset(self):
        dataset = { "name":  self.name,
                    "type":  self.hydra_data_type,
                    "value": self.value,
                    "metadata": "{}",
                    "unit": "-",
                    "hidden": 'N'
                  }
        return dataset



class PywrNode(PywrEntity):
    node_type_map = {}
    base_attrs = ("name", "comment", "position")

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        PywrNode.node_type_map[cls.key] = cls

    def __init__(self, data, **kwargs):
        #print(data)
        self.name = data["name"]
        location = data.get("position")
        self.position = PywrPosition.PywrPositionFactory(location) if location else None
        self.comment = data.get("comment")

    @staticmethod
    def NodeFactory(data):
        instkey = data["type"]
        instcls = PywrNode.node_type_map.get(instkey)
        if instcls:
            return instcls(data)
        else:
            instcls = PywrNode.node_type_map["__custom_node__"]
            return instcls(data)

    @property
    def has_unresolved_parameter_reference(self):
        refs = filter(lambda a: isinstance(a, PywrParameterReference), self.__dict__.values())
        return any(refs)

    @property
    def unresolved_parameter_references(self):
        return [*filter(lambda i: isinstance(i[1], PywrParameterReference), self.__dict__.items())]

    """
    def set_data_reference(name, data):
        inst = PywrDataReference.ReferenceFactory()
    """


class PywrEdge(PywrEntity):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        edge_types.append(cls)

    def __init__(self, data):
        super().__init__()
        self.src = data[0]
        self.dest = data[1]
        self.name = f"{self.src} to {self.dest}"


class PywrParameter(PywrEntity, HydraDataset):
    parameter_type_map = {}
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        PywrParameter.parameter_type_map[cls.key] = cls

    @staticmethod
    def ParameterFactory(arg): # (name, data) from params.items()
        instkey = arg[1]["type"]
        instcls = PywrParameter.parameter_type_map[instkey]
        return instcls(*arg)

    def __init__(self, name):
        self.name = name



class PywrRecorder(PywrEntity):
    recorder_type_map = {}
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        PywrRecorder.recorder_type_map[cls.key] = cls
        print(f"Registered {cls.key}")

    def __init__(self, name):
        self.name = name

    @staticmethod
    def RecorderFactory(arg): # (name, data)
        instkey = arg[1]["type"]
        instcls = PywrRecorder.recorder_type_map[instkey]
        return instcls(*arg)


class PywrDataReference(PywrEntity, ABC):

    @staticmethod
    def ReferenceFactory(name, data):
        if isinstance(data, dict):
            if data.get("type"):
                """ It looks like a Parameter, try to construct it as one... """
                try:
                    return PywrParameter.ParameterFactory(data)
                except KeyError:
                    pass

            """ ... it's just a dataframe."""
            return PywrDataframeReference(name, data)

        if isinstance(data, list):
            return PywrArrayReference(name, data)

        if isinstance(data, numbers.Number):
            return PywrScalarReference(name, data)

        if isinstance(data, str):
            """ Could be either...
                    - A reference to a __node__:attr param key
                    - A plain descriptor
            """
            try:
                elem_name, attr = parse_reference_key(data)
                return PywrParameterReference(data)
            except ValueError as e:
                pass
            """ ... it's just a descriptor """
            return PywrDescriptorReference(name, data)

        # Handle unparseable case

    def __init__(self, name):
        self.name = name

    @property
    @abstractmethod
    def value(self):
        pass

    @property
    def dataset(self):
        dataset = { "name":  self.name,
                    "type":  self.hydra_data_type,
                    "value": json.dumps(self.value),
                    "metadata": "{}",
                    "unit": "-",
                    "hidden": 'N'
                  }
        return dataset


class PywrDescriptorReference(PywrDataReference):
    hydra_data_type = "DESCRIPTOR"
    def __init__(self, name, data):
        super().__init__(name)
        self._value = data

    @property
    def value(self):
        return self._value

class PywrArrayReference(PywrDataReference):
    hydra_data_type = "ARRAY"
    def __init__(self, name, data):
        super().__init__(name)
        self._value = data

    @property
    def value(self):
        return self._value

class PywrScalarReference(PywrDataReference):
    hydra_data_type = "SCALAR"
    def __init__(self, name, data):
        super().__init__(name)
        self._value = data

    @property
    def value(self):
        return self._value

class PywrDataframeReference(PywrDataReference):
    hydra_data_type = "DATAFRAME"
    def __init__(self, name, data):
        super().__init__(name)
        self._value = data

    @property
    def value(self):
        return self._value

class PywrParameterReference(PywrDataReference):
    def __init__(self, name):
        super().__init__(name)
        self._value = name

    @property
    def value(self):
        return self._value
