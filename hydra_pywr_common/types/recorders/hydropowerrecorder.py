from hydra_pywr_common.types.mixins import ArbitraryDirectAttrs

from hydra_pywr_common.types import(
    PywrRecorder
)

class PywrHydroPowerRecorder(PywrRecorder, ArbitraryDirectAttrs):
    key = "hydropowerrecorder"
    hydra_data_type = "PYWR_RECORDER"

    def __init__(self, name, data):
        super().__init__(name)
        #self.node = data["node"]

        #if "is_objective" in data:
        #    self.is_objective = data.get("is_objective")

        self.add_attrs(data)


    @property
    def value(self):
        """
        rec = { "type": self.key,
                "node": self.node,
              }
        if hasattr(self, "is_objective"):
            rec.update({ "is_objective": self.is_objective })

        return rec
        """
        ret = self.get_attr_values()
        ret.update({ "type": self.key })
        return ret
