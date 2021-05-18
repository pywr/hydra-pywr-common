"""
Base types for model types
"""

import json
import numbers
from abc import ABC, abstractmethod

from hydra_pywr_common.lib.utils import(
    parse_reference_key
)

from .fragments.position import(
    PywrPosition
)

from .mixins import(
    HydraDataset
)


class PywrEntity():
    """ Base type for all elements capable of
        appearing in a Pywr network
    """
    pass

"""
class HydraDataset():

    def attr_dataset(self, attr_name):
        attr = getattr(self, attr_name)
        dataset = { "name":  attr_name,
                    "type":  attr.hydra_data_type,
                    "value": attr.value,
                    "metadata": "{}",
                    "unit": "-",
                    "hidden": 'N'
                  }
        return dataset
"""


class PywrNode(PywrEntity, HydraDataset):
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
        self.comment = data.get("comment", "")
        self.intrinsic_attrs = []
        #if self.name == "Gitaru":
        #    print(data)
        #    exit(55)
        self.parse_data(data)

    @staticmethod
    def NodeFactory(data):
        instkey = data["type"]
        instcls = PywrNode.node_type_map.get(instkey)
        if instcls:
            return instcls(data)

        else:
            instcls = PywrNode.node_type_map["__custom_node__"]
            return instcls(data)

    def parse_data(self, data):
        for attrname, value in data.items():
            #if self.name == "Aggregated Demand":
            #    import pudb; pudb.set_trace()
            if attrname in PywrNode.base_attrs:
                continue

            typed_attr = PywrDataReference.ReferenceFactory(attrname, value)
            setattr(self, attrname, typed_attr)
            self.intrinsic_attrs.append(attrname)

    @property
    def has_unresolved_parameter_reference(self):
        refs = filter(lambda a: isinstance(a, PywrParameterReference), self.__dict__.values())
        return any(refs)

    @property
    def unresolved_parameter_references(self):
        return [*filter(lambda i: isinstance(i[1], PywrParameterReference), self.__dict__.items())]

    @property
    def parameters(self):
        param_insts = filter(lambda a: isinstance(a, PywrParameter), self.__dict__.values())
        return {f"__{self.name}__:{inst.name}": inst for inst in param_insts}

    @property
    def recorders(self):
        rec_insts = filter(lambda a: isinstance(a, PywrRecorder), self.__dict__.values())
        return {f"__{self.name}__:{inst.name}": inst for inst in rec_insts}

    @property
    def pywr_node(self):
        node = { "name": self.name,
                 "comment": self.comment
               }

        if self.position is not None:
             node.update({"position": self.position.value})

        intrinsics = { name: attr.value for name, attr in self.__dict__.items() if name in self.intrinsic_attrs and not isinstance(getattr(self, name), PywrParameter) }
        param_refs = {}
        for param_attr in self.parameters.keys():
            node_name, attr_name = parse_reference_key(param_attr)
            param_refs[attr_name] = param_attr

        node.update(intrinsics)
        node.update(param_refs)

        return node

    @property
    def pywr_json(self):
        return json.dumps(self.pywr_node)




class PywrEdge(PywrEntity):
    key = "edge"
    """
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        edge_types.append(cls)
    """

    def __init__(self, data):
        super().__init__()
        """
            Characterise edge type
              - Standard
              - Slotted
              - Piecewise???
        """
        if len(data) == 2:  # [ src, dest ]
            self.src = data[0]
            self.dest = data[1]
            self.name = f"{self.src} to {self.dest}"
        elif len(data) == 4:  # [ src, dest, src_slot:int, dest_slot:int ]
            self.src = data[0]
            self.dest = data[1]
            self.src_slot = data[2]
            self.dest_slot = data[3]
            self.name = f"{self.src}:{self.src_slot} to {self.dest}:{self.dest_slot}"


    @property
    def value(self):
        if hasattr(self, "src_slot"):
            return [ self.src, self.dest, self.src_slot, self.dest_slot ]

        return [ self.src, self.dest ]


class PywrParameter(PywrEntity):
    #hydra_data_type = "PYWR_PARAMETER"
    parameter_type_map = {}
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        PywrParameter.parameter_type_map[cls.key.lower()] = cls

    @staticmethod
    def ParameterFactory(arg): # (name, data) from params.items()
        instkey = arg[1]["type"]
        instcls = PywrParameter.parameter_type_map[instkey.lower()]
        return instcls(*arg)

    def __init__(self, name):
        self.name = name

    def attr_dataset(self, attr_name):
        attr = getattr(self, attr_name)
        value = attr.value
        del value["type"]
        dataset = { "name":  attr_name,
                    "type":  attr.hydra_data_type,
                    "value": json.dumps(value),
                    "metadata": "{}",
                    "unit": "-",
                    "hidden": 'N'
                  }
        return dataset



class PywrRecorder(PywrEntity):
    recorder_type_map = {}
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        PywrRecorder.recorder_type_map[cls.key] = cls

    def __init__(self, name):
        self.name = name

    @staticmethod
    def RecorderFactory(arg): # (name, data)
        instkey = arg[1]["type"]
        instcls = PywrRecorder.recorder_type_map[instkey.lower()]
        return instcls(*arg)


class PywrDataReference(PywrEntity, ABC):

    @staticmethod
    def ReferenceFactory(name, data):
        #print(f"ReferenceFactory {name} {type(data)}")
        #print(data)
        if isinstance(data, dict):
            if data.get("type"):
                """ It looks like a Parameter, try to construct it as one... """
                try:
                    return PywrParameter.ParameterFactory((name, data)) # NB tuple
                    #return PywrParameterReference(data)
                except KeyError:
                    """ ...no match as param. maybe recorder?... """
                    return PywrRecorder.RecorderFactory((name, data))

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
        return PywrDescriptorReference(name, "")

    def __init__(self, name):
        self.name = name

    @property
    @abstractmethod
    def value(self):
        pass

    """
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
    """


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
        return json.dumps(self._value)

class PywrParameterReference(PywrDataReference):
    def __init__(self, name):
        super().__init__(name)
        self._value = name

    @property
    def value(self):
        return self._value

class PywrRecorderReference(PywrDataReference):
    def __init__(self, name):
        super().__init__(name)
        self._value = name

    @property
    def value(self):
        return self._value
