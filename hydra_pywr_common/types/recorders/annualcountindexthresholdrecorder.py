from hydra_pywr_common.types import(
    PywrRecorder
)

class PywrAnnualCountIndexThresholdRecorder(PywrRecorder):
    key = "annualcountindexthresholdrecorder"
    hydra_data_type = "PYWR_RECORDER"

    def __init__(self, name, data):
        super().__init__(name)
        self.parameters = data["parameters"]
        self.threshold = data["threshold"]


    @property
    def value(self):
        return { "type": self.key,
                 "parameters": self.parameters,
                 "threshold": self.threshold
               }
