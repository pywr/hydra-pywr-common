from .base import Fragment
from hydra_pywr_common.types.base import(
    PywrDataReference,
    PywrDescriptorReference
)

class Timestepper(Fragment):
    def __init__(self, data):
        super().__init__()
        self.parse_data(data)

    def parse_data(self, data):
        for attrname, value in data.items():
            typed_attr = PywrDataReference.ReferenceFactory(attrname, value)
            setattr(self, attrname, typed_attr)
            self.intrinsic_attrs.append(attrname)

    """ Override base get_values to intify timestep """
    def get_values(self):
        values = super().get_values()
        timestep = values.get("timestep")
        try:
            ts_val = int(float(timestep))
        except ValueError:
            ts_val = timestep
        values["timestep"] = ts_val
        return values


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
        self.set_intrinsic_as(PywrDescriptorReference, "index_col", data)
        self.set_intrinsic_as(PywrDescriptorReference, "header", data)
        self.parse_data(data)

    def parse_data(self, data):
        for attrname, value in data.items():
            typed_attr = PywrDataReference.ReferenceFactory(attrname, value)
            setattr(self, attrname, typed_attr)
            self.intrinsic_attrs.append(attrname)

    """ Override base get_values to force types """
    def get_values(self):
        values = super().get_values()
        for attr in ("index_col", "header"):
            if attr not in values:
                continue
            val = values.get(attr)
            try:
                t_val = int(float(val))
            except ValueError:
                t_val = val
            values[attr] = t_val

        if "parse_dates" in values:
            parse_dates = values.get("parse_dates")
            try:
                t_val = parse_dates == "True"
            except ValueError:
                t_val = timestep
            values["parse_dates"] = t_val

        return values
