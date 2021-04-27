import pandas as pd
from hydra_pywr_common.types import PywrParameter

class PywrDataframeParameter(PywrParameter):
    key = "dataframeparameter"

    def __init__(self, argdata, **kwargs):
        basekey = next(iter(argdata))
        datakey = next(iter(argdata[basekey]))

        data = argdata[basekey][datakey]
        self.set_value(data)


    def set_value(self, data):
        self.value = pd.DataFrame.from_dict(data, orient="index")


