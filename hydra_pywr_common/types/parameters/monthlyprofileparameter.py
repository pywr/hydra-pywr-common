from hydra_pywr_common.types import PywrParameter
from hydra_pywr_common.lib.utils import(
    parse_reference_key
)

class PywrMonthlyProfileParameter(PywrParameter):
    key = "monthlyprofile"

    def __init__(self, name, data, **kwargs):
        super().__init__(name)
        self.set_value(data)
        """
        key, data = argdata
        name, attr = parse_reference_key(key)

        self.set_value(data)
        """


    def set_value(self, data):
        self._value = data["values"]

    @property
    def value(self):
        return { "type": self.key,
                 "values": self._value
               }


