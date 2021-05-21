from hydra_pywr_common.types import PywrParameter
from hydra_pywr_common.types.mixins import ArbitraryDirectAttrs

class PywrDailyProfileParameter(PywrParameter, ArbitraryDirectAttrs):
    key = "dailyprofile"
    hydra_data_type = "PYWR_PARAMETER"

    def __init__(self, name, data, **kwargs):
        super().__init__(name)
        self.add_attrs(data)
        #self.set_value(data)

    def set_value(self, data):
        """
        for attr, val in data.items():
        if "table" in data:
            self.table = data["table"]
            self.column = data["column"]
        else:
            self._value = data["values"]
        """

    @property
    def value(self):
        """
        ret =  { "type": self.key }

        if hasattr(self, "table"):
            ret.update( { "table": self.table,
                          "column": self.column
                        })
        else:
            ret.update( {"values": self._value})
        """
        ret = self.get_attr_values()
        ret.update( {"type": self.key} )
        return ret


"""
    Fix multiple names for PYWR_DAILY_PROFILE_PARAMETER
"""
PywrParameter.parameter_type_map["dailyprofileparameter"] = PywrDailyProfileParameter
