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
