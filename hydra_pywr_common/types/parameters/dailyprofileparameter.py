from hydra_pywr_common.types import PywrParameter
from hydra_pywr_common.lib.utils import(
    parse_reference_key
)

class PywrDailyProfileParameter(PywrParameter):
    key = "dailyprofile"

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


"""
    Fix multiple names for PYWR_DAILY_PROFILE_PARAMETER
"""
PywrParameter.parameter_type_map["dailyprofileparameter"] = PywrDailyProfileParameter
