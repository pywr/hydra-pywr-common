from hydra_pywr_common.types import PywrParameter

class PywrInterpolatedFlowParameter(PywrParameter):
    key = "interpolatedflowparameter"

    def __init__(self, name, data, **kwargs):
        super().__init__(name)

        self.node = data["node"]
        self.flows = data["flows"]
        self.values = data["values"]
        self.__recorder__ = data["__recorder__"]


    @property
    def value(self):
        return { "type": self.key,
                 "node": self.node,
                 "flows": self.flows,
                 "values": self.values,
                 "__recorder__": self.__recorder__
               }


