from hydra_pywr_common.types import PywrParameter
from hydra_pywr_common.types.mixins import ArbitraryDirectAttrs

class PywrHydroPowerTargetParameterWithVaribaleTailwater(PywrParameter, ArbitraryDirectAttrs):
    key = "hydropowertargetparameterwithvaribaletailwater"
    hydra_data_type = "PYWR_PARAMETER"
    """
    def __init__(self, name, data, **kwargs):
        super().__init__(name)
        self.set_value(data)


    def set_value(self, data):
        self._value = data["value"]
    """
    def __init__(self, name, data, **kwargs):
        super().__init__(name)
        self.add_attrs(data)

    """
    @property
    def value(self):
        return { "type": self.key,
                 "value": self._value
               }
    """
    @property
    def value(self):
        ret = self.get_attr_values()
        ret.update( {"type": self.key} )
        return ret


PywrParameter.parameter_type_map["hydropowertargetparameterwithvaribaletailwater_"] = PywrHydroPowerTargetParameterWithVaribaleTailwater
PywrParameter.parameter_type_map["hydropowertargetparameterwithvaribaletailwaterparameter"] = PywrHydroPowerTargetParameterWithVaribaleTailwater
