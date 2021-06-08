from hydra_pywr_common.types import PywrParameter

class PywrMonthlyProfileParameter(PywrParameter):
    key = "monthlyprofileparameter"
    hydra_data_type = "PYWR_PARAMETER_MONTHLY_PROFILE"

    def __init__(self, name, data, **kwargs):
        super().__init__(name)
        self.set_value(data)

    def set_value(self, data):
        self._value = data["values"]

    @property
    def value(self):
        return { "type": self.key,
                 "values": self._value
               }

