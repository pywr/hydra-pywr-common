import pandas as pd
from hydra_pywr_common.types import PywrParameter

class PywrDataframeParameter(PywrParameter):
    key = "dataframeparameter"
    hydra_data_type = "PYWR_DATAFRAME"

    def __init__(self, argdata, **kwargs):
        basekey = next(iter(argdata))
        datakey = next(iter(argdata[basekey]))

        data = argdata[basekey][datakey]
        self.set_value(data)
        self.name = basekey


    def set_value(self, data):
        self.value = pd.DataFrame.from_dict(data, orient="index")


    # TODO pandas kwargs
