from hydra_pywr_common.types import PywrParameter
from hydra_pywr_common.lib.utils import(
    parse_parameter_key
)

class PywrMonthlyProfileParameter(PywrParameter):
    key = "monthlyprofile"

    def __init__(self, argdata, **kwargs):
        self.set_value(argdata)
        """
        key, data = argdata
        name, attr = parse_parameter_key(key)

        self.set_value(data)
        """


    def set_value(self, data):
        self.value = data["values"]


