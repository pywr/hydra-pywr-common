from hydra_pywr_common.types import PywrParameter

class PywrAggregatedParameter(PywrParameter):
    key = "aggregatedparameter"

    def __init__(self, name, data, **kwargs):
        super().__init__(name)
        self.set_value(data)

    def set_value(self, data):
        self.agg_func = data["agg_func"]
        self.parameters = data["parameters"]

    @property
    def value(self):
        return { "type": self.key,
                "agg_func": self.agg_func,
                 "parameters": self.parameters
               }
