from hydra_pywr_common.types.mixins import HydraDataset

class Fragment():
    """ Base of all Pywr Fragments """
    def __init__(self):
        self.intrinsic_attrs = []


    def attr_dataset(self, attr_name):
        base, local_attr = attr_name.split('.')
        attr = getattr(self, local_attr)
        dataset = { "name":  attr_name,
                    "type":  attr.hydra_data_type,
                    "value": attr.value,
                    "metadata": "{}",
                    "unit": "-",
                    "hidden": 'N'
                  }
        return dataset
