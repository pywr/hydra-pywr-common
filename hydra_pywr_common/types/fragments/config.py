from .base import Fragment

from hydra_pywr_common.types.base import(
    PywrDataReference,
    PywrDescriptorReference
)

class IntegratedConfig(Fragment):
    def __init__(self, data):
        super().__init__()
        self.parse_data(data)

    def parse_data(self, data):
        for attrname, value in data.items():
            typed_attr = PywrDataReference.ReferenceFactory(attrname, value)
            setattr(self, attrname, typed_attr)
            self.intrinsic_attrs.append(attrname)
