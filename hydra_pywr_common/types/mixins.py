import json

class HydraDataset():

    def attr_dataset(self, attr_name):
        attr_inst = getattr(self, attr_name)
        value = attr_inst.get_value()
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        dataset = {
            "name":  attr_name,
            "type":  attr_inst.hydra_data_type,
            "value": value,
            "metadata": "{}",
            "unit": "-",
            "hidden": 'N'
        }
        return dataset


class ArbitraryDirectAttrs():
    def __init__(self):
        super().__init__()
        self.intrinsics = set()

    def add_attrs(self, data):
        for attr, val in data.items():
            setattr(self, attr, val)
            self.intrinsics.add(attr)

    def get_attr_values(self):
        return {attr: getattr(self, attr) for attr in self.intrinsics}
