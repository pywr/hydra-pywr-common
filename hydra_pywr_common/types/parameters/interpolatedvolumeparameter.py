from hydra_pywr_common.types import PywrParameter

class PywrInterpolatedVolumeParameter(PywrParameter):
    key = "interpolatedvolumeparameter"
    hydra_data_type = "PYWR_PARAMETER"

    def __init__(self, name, data, **kwargs):
        super().__init__(name)

        self.node = data["node"]
        self.volumes = data["volumes"]
        self.values = data["values"]
        self.kind = data["kind"]


    @property
    def value(self):
        return { "type": self.key,
                 "node": self.node,
                 "volumes": self.volumes,
                 "values": self.values,
                 "kind": self.kind
               }


