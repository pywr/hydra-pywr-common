from hydra_pywr_common.types import PywrParameter

class PywrControlCurveInterpolatedParameter(PywrParameter):
    key = "controlcurveinterpolated"
    hydra_data_type = "PYWR_PARAMETER_CONTROL_CURVE_INTERPOLATED"

    def __init__(self, name, data, **kwargs):
        super().__init__(name)

        self.storage_node = data["storage_node"]
        self.control_curves = data["control_curves"]
        self.values = data["values"]
        self.__recorder__ = data["__recorder__"]


    @property
    def value(self):
        return { "type": self.key,
                 "storage_node": self.storage_node,
                 "control_curves": self.control_curves,
                 "values": self.values,
                 "__recorder__": self.__recorder__
               }


