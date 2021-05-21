import json

class HydraDataset():

    def attr_dataset(self, attr_name):
        attr_inst = getattr(self, attr_name)
        value = attr_inst.value
        if isinstance(value, dict):
            #del value["type"]
            value = json.dumps(value)
        if isinstance(value, list):
            value = json.dumps(value)
        dataset = { "name":  attr_name,
                    "type":  attr_inst.hydra_data_type,
                    "value": value,
                    "metadata": "{}",
                    "unit": "-",
                    "hidden": 'N'
                  }
        return dataset

class ArbitraryDirectAttrs():

    def add_attrs(self, data):
        self.intrinsics = set()
        for attr, val in data.items():
            setattr(self, attr, val)
            self.intrinsics.add(attr)

    def get_attr_values(self):
        return { getattr(self, attr) for attr in self.intrinsics() }
