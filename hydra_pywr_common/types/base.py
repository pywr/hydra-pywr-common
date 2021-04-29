"""
Base types for model types
"""

import json
import numbers
from abc import ABC, abstractmethod

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

    """
    def set_data_reference(name, data):
        inst = PywrDataReference.ReferenceFactory()
    """


class PywrEdge(PywrEntity):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        edge_types.append(cls)


class PywrParameter(PywrEntity, HydraDataset):
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
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        recorder_types.append(cls)


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
