from hydra_pywr_common.types import PywrParameter

class PywrControlCurveHoldIndexParameter(PywrParameter):
    key = "controlcurveholdindexparameter"
    hydra_data_type = "PYWR_PARAMETER"

    def __init__(self, name, data, **kwargs):
        super().__init__(name)

        self.storage_node = data["storage_node"]
        self.control_curves = data["control_curves"]
        self.minimum_days_in_level = data["minimum_days_in_level"]


    @property
    def value(self):
        return { "type": self.key,
                 "storage_node": self.storage_node,
                 "control_curves": self.control_curves,
                 "minimum_days_in_level": self.minimum_days_in_level
               }

PywrParameter.parameter_type_map["controlcurveholdindex"] = PywrControlCurveHoldIndexParameter
