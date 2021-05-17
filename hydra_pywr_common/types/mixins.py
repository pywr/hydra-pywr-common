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
