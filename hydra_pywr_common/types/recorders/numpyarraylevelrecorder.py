from hydra_pywr_common.types import(
    PywrRecorder,
    PywrDataReference
)

class PywrNumpyArrayLevelRecorder(PywrRecorder):
    key = "numpyarraylevelrecorder"
    hydra_data_type = "PYWR_RECORDER"

    def __init__(self, name, data):
        super().__init__(name)
        self.node = data["node"]

        if "is_objective" in data:
            self.is_objective = data.get("is_objective")

    @property
    def value(self):
        rec = { "type": self.key,
                "node": self.node,
              }
        if hasattr(self, "is_objective"):
            rec.update({ "is_objective": self.is_objective })

        return rec
