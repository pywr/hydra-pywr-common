from hydra_pywr_common.types import(
    PywrRecorder,
    PywrDataReference
)

class PywrRollingMeanFlowNodeRecorder(PywrRecorder):
    key = "rollingmeanflownoderecorder"
    hydra_data_type = "PYWR_RECORDER"

    def __init__(self, name, data):
        super().__init__(name)
        self.node = data["node"]
        self.timesteps = int(data["timesteps"])

    @property
    def value(self):
        return { "type": self.key,
                 "node": self.node,
                 "timesteps": self.timesteps
               }
