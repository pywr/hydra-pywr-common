from hydra_pywr_common.types import(
    PywrRecorder,
    PywrDataReference
)

class PywrNumpyArrayNodeRecorder(PywrRecorder):
    key = "NumpyArrayNodeRecorder"

    def __init__(self, name, data):
        super().__init__(name)
        self.node = data["node"]
        self.is_objective = data["is_objective"]
