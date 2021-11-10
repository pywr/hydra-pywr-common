from hydra_pywr_common.types import PywrParameter

class PywrControlCurveIndexParameter(PywrParameter):
    key = "controlcurveindexparameter"
    hydra_data_type = "PYWR_PARAMETER_CONTROL_CURVE_INDEX"

    def __init__(self, name, data, **kwargs):
        super().__init__(name)

        self.storage_node = data["storage_node"]
        self.control_curves = data["control_curves"]


    @property
    def value(self):
        return { "type": self.key,
                 "storage_node": self.storage_node,
                 "control_curves": self.control_curves,
               }

