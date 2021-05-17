from hydra_pywr_common.types import(
    PywrRecorder,
    PywrDataReference
)

class PywrFlowDurationCurveRecorder(PywrRecorder):
    key = "flowdurationcurverecorder"
    hydra_data_type = "PYWR_RECORDER_FDC"

    def __init__(self, name, data):
        super().__init__(name)
        self.node = data["node"]
        self.percentiles = PywrDataReference.ReferenceFactory("percentiles", data["percentiles"])

    @property
    def value(self):
        return { "type": self.key,
                 "node": self.node,
                 "percentiles": self.percentiles.value
               }
