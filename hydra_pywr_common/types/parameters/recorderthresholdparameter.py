from hydra_pywr_common.types import PywrParameter

class PywrRecorderThresholdParameter(PywrParameter):
    key = "recorderthreshold"

    def __init__(self, name, data, **kwargs):
        super().__init__(name)

        self.recorder = data["recorder"]
        self.threshold = data["threshold"]
        self.values = data["values"]
        self.predicate = data["predicate"]


    @property
    def value(self):
        return { "type": self.key,
                 "recorder": self.recorder,
                 "threshold": self.threshold,
                 "values": self.values,
                 "predicate": self.predicate
               }


