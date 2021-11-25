from hydra_pywr_common.types import PywrParameter
from hydra_pywr_common.types.mixins import ArbitraryDirectAttrs

class PywrUnknownParameter(PywrParameter, ArbitraryDirectAttrs):
    hydra_data_type = "PYWR_PARAMETER"
    _data = {}

    def __init__(self, name, data, **kwargs):
        super().__init__(name)
        self.data = data

    def get_value(self):
        return self.data
