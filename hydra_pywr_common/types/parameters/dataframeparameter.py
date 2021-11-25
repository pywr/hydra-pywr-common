from hydra_pywr_common.types import PywrParameter
from hydra_pywr_common.types.mixins import ArbitraryDirectAttrs

class PywrDataframeParameter(PywrParameter, ArbitraryDirectAttrs):
    key = "dataframeparameter"
    hydra_data_type = "PYWR_DATAFRAME"

    def __init__(self, name, argdata, **kwargs):
        super().__init__(name)

        if "data" in argdata:
            data = argdata.get("data")
            self.basekey = next(iter(data))  # The first key in data dict
            series = data[self.basekey]
            self.set_value(series)
            self.pandas_kwargs = argdata.get("pandas_kwargs", {})
        else:
            self.add_attrs(argdata)


    def set_value(self, data):
        self._value = data

    @property
    def value(self):
        if hasattr(self, "_value"):
            return {
                     "data": { self.basekey: self._value}
                   }
        else:
            ret = self.get_attr_values()
            return ret

