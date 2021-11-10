
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


    def set_intrinsic_as(self, cls, attr_name, data):
        attr = cls(attr_name, data.pop(attr_name))
        setattr(self, attr_name, attr)
        self.intrinsic_attrs.append(attr_name)


    def get_values(self):
        return { attr_name: getattr(self, attr_name).value for attr_name in self.intrinsic_attrs }
