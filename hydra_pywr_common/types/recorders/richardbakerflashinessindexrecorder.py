from hydra_pywr_common.types.mixins import ArbitraryDirectAttrs

from hydra_pywr_common.types import(
    PywrRecorder
)

class PywrRichardBakerFlashinessIndexRecorder(PywrRecorder, ArbitraryDirectAttrs):
    key = "RichardBakerFlashinessIndexRecorder"
    hydra_data_type = "PYWR_RECORDER"

    def __init__(self, name, data):
        super().__init__(name)

        """
        if "is_objective" in data:
            self.is_objective = data.get("is_objective")
        if "node" in data:
            self.node = data.get("node")
        """

        self.add_attrs(data)


    @property
    def value(self):
        ret = self.get_attr_values()
        ret.update({ "type": self.key })
        return ret
