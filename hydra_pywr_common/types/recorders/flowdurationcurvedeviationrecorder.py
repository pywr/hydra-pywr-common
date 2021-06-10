from hydra_pywr_common.types import(
    PywrRecorder,
    PywrDataReference
)

class PywrFlowDurationCurveDeviationRecorder(PywrRecorder):
    key = "flowdurationcurvedeviationrecorder"
    hydra_data_type = "PYWR_RECORDER_FDC_DEVIATION"

    def __init__(self, name, data):
        super().__init__(name)
        self.node = data["node"]
        self.percentiles = PywrDataReference.ReferenceFactory("percentiles", data["percentiles"])
        self.lower_target_fdc = PywrDataReference.ReferenceFactory("lower_target_fdc", data["lower_target_fdc"])
        self.upper_target_fdc = PywrDataReference.ReferenceFactory("upper_target_fdc", data["upper_target_fdc"])

    @property
    def value(self):
        return { "type": self.key,
                 "node": self.node,
                 "percentiles": self.percentiles.value,
                 "lower_target_fdc": self.lower_target_fdc.value,
                 "upper_target_fdc": self.upper_target_fdc.value
               }
