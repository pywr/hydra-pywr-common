from hydra_pywr_common.types import(
    PywrRecorder,
    PywrDataReference
)

class PywrFlowDurationCurveRecorder(PywrRecorder):
    key = "flowdurationcurverecorder"

    def __init__(self, name, data):
        super().__init__(name)
        self.node = data["node"]
        self.percentiles = PywrDataReference.ReferenceFactory("percentiles", data["percentiles"])
