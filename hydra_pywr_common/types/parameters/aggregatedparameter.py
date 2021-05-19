from hydra_pywr_common.types import PywrParameter

class PywrAggregatedParameter(PywrParameter):
    key = "aggregatedparameter"
    hydra_data_type = "PYWR_PARAMETER_AGGREGATED"

    def __init__(self, name, data, **kwargs):
        super().__init__(name)
        self.set_value(data)

    def set_value(self, data):
        self.agg_func = data["agg_func"]
        self.parameters = data["parameters"]
        if "__recorder__" in data:
            self.__recorder__ = data["__recorder__"]

        breakpoint()

    @property
    def value(self):
        ret = { "type": self.key,
                "agg_func": self.agg_func,
                "parameters": self.parameters
              }
        if hasattr(self, "__recorder__"):
            ret["__recorder__"] = self.__recorder__

        return ret
