import pandas as pd
from hydra_pywr_common.types import PywrParameter

class PywrDataframeParameter(PywrParameter):
    key = "dataframeparameter"
    hydra_data_type = "PYWR_DATAFRAME"

    def __init__(self, name, argdata, **kwargs):
        super().__init__(name)
        basekey = next(iter(argdata))
        datakey = next(iter(argdata[basekey]))

        data = argdata[basekey][datakey]
        self.set_value(data)

        self.pandas_kwargs = argdata.get("pandas_kwargs", {})


    def set_value(self, data):
        #self._value = pd.DataFrame.from_dict(data, orient="index")
        self._value = data

    @property
    def value(self):
        """
        if hasattr(self, "_value"):
            return self._value.to_json()
        """
        print(self._value)
        return { "type": self.key,
                 "data": { self.name: self._value},
                 "pandas_kwargs": self.pandas_kwargs
               }

