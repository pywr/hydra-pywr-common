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


class PywrNode(PywrEntity, HydraDataset):
    node_type_map = {}
    base_attrs = ("name", "comment", "position")

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        PywrNode.node_type_map[cls.key] = cls

    def __init__(self, data, **kwargs):
        self.name = data["name"]
        location = data.get("position")
        self.position = PywrPosition(location) if location else None
        if "comment" in data:
            self.comment = data.get("comment")
        self.intrinsic_attrs = []
        self.parse_data(data)

    def __len__(self):
        return len(self.name)

    @staticmethod
    def NodeFactory(data):
        instkey = data["type"].lower()
        instcls = PywrNode.node_type_map.get(instkey)
        if instcls:
            return instcls(data)

        else:
            instcls = PywrNode.node_type_map["__custom_node__"]
            return instcls(data)

    def parse_data(self, data):
        for attrname, value in data.items():
            if attrname in PywrNode.base_attrs:
                continue

            typed_attr = PywrDataReference.ReferenceFactory(attrname, value)
            setattr(self, attrname, typed_attr)
            self.intrinsic_attrs.append(attrname)

    @property
    def has_unresolved_parameter_reference(self):
        refs = filter(lambda a: isinstance(a, PywrDescriptorReference), self.__dict__.values())
        return any(refs)

    @property
    def unresolved_parameter_references(self):
        return [*filter(lambda i: isinstance(i[1], PywrDescriptorReference), self.__dict__.items())]

    @property
    def parameters(self):
        param_insts = filter(lambda a: isinstance(a, PywrParameter), self.__dict__.values())
        return {f"__{self.name}__:{inst.name}": inst for inst in param_insts}

    @property
    def recorders(self):
        rec_insts = filter(lambda a: isinstance(a, PywrRecorder), self.__dict__.values())
        return {f"__{self.name}__:{inst.name}": inst for inst in rec_insts}

    def _attr_is_p_or_r(self, attr):
        ref = getattr(self, attr)
        return isinstance(ref, (PywrParameter, PywrRecorder))

    @property
    def pywr_node(self, inline_refs = False):
        node = {"name": self.name}

        if hasattr(self, "comment") and self.comment is not None:
            node.update({"comment": self.comment})

        if hasattr(self, "position") and self.position is not None and self.position.is_not_null:
            node.update({"position": self.position.value})

        intrinsics = { name: attr.get_value() for name, attr in self.__dict__.items() if name in self.intrinsic_attrs and not self._attr_is_p_or_r(name) }
        param_refs = {}
        for param_attr in self.parameters:
            node_name, attr_name = parse_reference_key(param_attr)
            if "flow" in attr_name:
                param_refs[attr_name] = param_attr

        recorder_refs = {}
        for rec_attr in self.recorders:
            node_name, attr_name = parse_reference_key(rec_attr)
            recorder_refs[attr_name] = rec_attr

        node.update(intrinsics)
        node.update(param_refs)

        return node

    @property
    def pywr_json(self):
        return json.dumps(self.pywr_node)


class PywrEdge(PywrEntity):
    key = "edge"

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
    hydra_data_type = "PYWR_PARAMETER"

    def __init__(self, name, data):
        super().__init__()
        self.name = name
        self.data = data

    def get_value(self):
        return self.data

    def attr_dataset(self, attr_name):
        dataset = {
            "name":  attr_name,
            "type":  self.hydra_data_type,
            "value": json.dumps(self.data),
            "metadata": "{}",
            "unit": "-",
            "hidden": 'N'
        }
        return dataset

    def as_dataset(self):
        dataset = {
            "name":  self.name,
            "type":  self.hydra_data_type,
            "value": json.dumps(self.data),
            "metadata": "{}",
            "unit": "-",
            "hidden": 'N'
        }
        return dataset


class PywrRecorder(PywrEntity):
    hydra_data_type = "PYWR_RECORDER"

    recorder_type_map = {}

    def get_value(self):
        return self.data

    def __init__(self, name, data):
        super().__init__()
        self.name = name
        self.data = data

    def as_dataset(self):
        dataset = {
            "name":  self.name,
            "type":  self.hydra_data_type,
            "value": json.dumps(self.data),
            "metadata": "{}",
            "unit": "-",
            "hidden": 'N'
        }
        return dataset

class PywrDataReference(PywrEntity, ABC):

    @staticmethod
    def ReferenceFactory(name, data):

        #Check to see if the data is a json-object encoded as a string
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except:
                pass

        if isinstance(data, dict):
            if data.get("type"):
                """ It looks like a Parameter, try to construct it as one... """
                if "recorder" in data['type'].lower():
                    return PywrRecorder(name, data)

                try:
                    return PywrParameter(name, data) # NB tuple
                except KeyError:
                    """ ...no match as param. maybe recorder?... """
                    return PywrRecorder(name, data)

            """ ... it's just a dataframe."""
            return PywrDataframeReference(name, data)

        if isinstance(data, list):
            return PywrArrayReference(name, data)

        if isinstance(data, bool):
            return PywrDescriptorReference(name, data)

        if isinstance(data, numbers.Number):
            return PywrScalarReference(name, data)

        if isinstance(data, str):
            """ Could be either...
                    - A reference to a __node__:attr param/rec key
                    - A plain descriptor
            """
            return PywrDescriptorReference(name, data)

        # Handle unparseable case
        return PywrDescriptorReference(name, "")

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_value(self):
        pass


class PywrDescriptorReference(PywrDataReference):
    hydra_data_type = "DESCRIPTOR"
    def __init__(self, name, data):
        super().__init__(name)
        self._value = data

    def get_value(self):
        return self._value

class PywrArrayReference(PywrDataReference):
    hydra_data_type = "ARRAY"
    def __init__(self, name, data):
        super().__init__(name)
        self._value = data

    def get_value(self):
        return self._value

class PywrScalarReference(PywrDataReference):
    hydra_data_type = "SCALAR"
    def __init__(self, name, data):
        super().__init__(name)
        self._value = data

    def get_value(self):
        return self._value

class PywrDataframeReference(PywrDataReference):
    hydra_data_type = "DATAFRAME"
    def __init__(self, name, data):
        super().__init__(name)
        self._value = data

    def get_value(self):
        return self._value

class PywrComponentReference(PywrDataReference):
    def __init__(self, name):
        super().__init__(name)
        self._value = name

    def get_value(self):
        return self._value

class PywrRecorderReference(PywrDataReference):
    def __init__(self, name):
        super().__init__(name)
        self._value = name

    def get_value(self):
        return self._value
