from .base import Fragment
from hydra_pywr_common.types.base import(
    PywrDataReference,
    PywrDescriptorReference
)

class Timestepper(Fragment):
    def __init__(self, data):
        super().__init__()
        #self.timestep = PywrDescriptorReference("timestep", data.pop("timestep"))
        self.set_intrinsic_as(PywrDescriptorReference, "timestep", data)
        self.parse_data(data)

    def parse_data(self, data):
        for attrname, value in data.items():
            typed_attr = PywrDataReference.ReferenceFactory(attrname, value)
            setattr(self, attrname, typed_attr)
            self.intrinsic_attrs.append(attrname)


class Metadata(Fragment):
    def __init__(self, data):
        super().__init__()
        self.parse_data(data)

    def parse_data(self, data):
        for attrname, value in data.items():
            typed_attr = PywrDataReference.ReferenceFactory(attrname, value)
            setattr(self, attrname, typed_attr)
            self.intrinsic_attrs.append(attrname)


class Table(Fragment):
    def __init__(self, data):
        super().__init__()
        #self.index_col = PywrDescriptorReference("index_col", data.pop("index_col"))
        #self.header = PywrDescriptorReference("header", data.pop("header"))
        self.set_intrinsic_as(PywrDescriptorReference, "index_col", data)
        self.set_intrinsic_as(PywrDescriptorReference, "header", data)
        self.parse_data(data)

    def parse_data(self, data):
        for attrname, value in data.items():
            typed_attr = PywrDataReference.ReferenceFactory(attrname, value)
            setattr(self, attrname, typed_attr)
            self.intrinsic_attrs.append(attrname)
