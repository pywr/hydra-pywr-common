from hydra_pywr_common.types import PywrParameter

class PywrCurrentDayThresholdParameter(PywrParameter):
    key = "currentdaythresholdparameter"
    hydra_data_type = "PYWR_PARAMETER"

    def __init__(self, name, data, **kwargs):
        super().__init__(name)

        self.threshold = data["threshold"]
        self.values = data["values"]
        self.predicate = data["predicate"]


    @property
    def value(self):
        return { "type": self.key,
                 "threshold": self.threshold,
                 "values": self.values,
                 "predicate": self.predicate
               }


