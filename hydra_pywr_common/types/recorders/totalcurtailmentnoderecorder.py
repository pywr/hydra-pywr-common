from hydra_pywr_common.types.mixins import ArbitraryDirectAttrs

from hydra_pywr_common.types import(
    PywrRecorder
)

class PywrTotalCurtailmentNodeRecorder(PywrRecorder, ArbitraryDirectAttrs):
    key = "totalcurtailmentnoderecorder"
    hydra_data_type = "PYWR_RECORDER"

    def __init__(self, name, data):
        super().__init__(name)
        self.add_attrs(data)


    @property
    def value(self):
        ret = self.get_attr_values()
        ret.update({ "type": self.key })
        return ret