from hydra_pywr_common.types import PywrParameter

class PywrAggregatedIndexParameter(PywrParameter):
    key = "aggregatedindexparameter"
    hydra_data_type = "PYWR_PARAMETER"

    def __init__(self, name, data, **kwargs):
        super().__init__(name)
        self.set_value(data)

    def set_value(self, data):
        self.agg_func = data["agg_func"]
        self.parameters = data["parameters"]
        if "__recorder__" in data:
            self.__recorder__ = data["__recorder__"]

    @property
    def value(self):
        ret = { "type": self.key,
                "agg_func": self.agg_func,
                "parameters": self.parameters
              }
        if hasattr(self, "__recorder__"):
            ret["__recorder__"] = self.__recorder__

        return ret
