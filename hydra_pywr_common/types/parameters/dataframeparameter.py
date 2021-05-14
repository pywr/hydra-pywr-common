import pandas as pd
from hydra_pywr_common.types import PywrParameter

class PywrDataframeParameter(PywrParameter):
    key = "dataframeparameter"
    hydra_data_type = "PYWR_DATAFRAME"

    def __init__(self, name, argdata, **kwargs):
        super().__init__(name)

        data = argdata.get("data")
        self.basekey = next(iter(data))  # The first key in data dict
        series = data[self.basekey]
        self.set_value(series)
        self.pandas_kwargs = argdata.get("pandas_kwargs", {})
        #print(f"{basekey=} {name=}")


    def set_value(self, data):
        #self._value = pd.DataFrame.from_dict(data, orient="index")
        self._value = data

    @property
    def value(self):
        return { "type": self.key,
                 "data": { self.basekey: self._value},
                 "pandas_kwargs": self.pandas_kwargs
               }

"""
    Fix multiple names in use for PYWR_DATAFRAME parameter
"""

PywrParameter.parameter_type_map["dataframe"] = PywrDataframeParameter
