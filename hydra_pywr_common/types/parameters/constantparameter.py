from hydra_pywr_common.types import PywrParameter

class PywrConstantParameter(PywrParameter):
    key = "constant"
    hydra_data_type = "PYWR_PARAMETER"

    def __init__(self, name, data, **kwargs):
        super().__init__(name)
        self.set_value(data)


    def set_value(self, data):
        self._value = data["value"]

    @property
    def value(self):
        return { "type": self.key,
                 "value": self._value
               }
