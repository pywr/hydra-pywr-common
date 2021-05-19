from hydra_pywr_common.types import PywrParameter

class PywrIndexedArrayParameter(PywrParameter):
    key = "indexedarrayparameter"
    hydra_data_type = "PYWR_PARAMETER_INDEXED_ARRAY"

    def __init__(self, name, data, **kwargs):
        super().__init__(name)

        self.index_parameter = data["index_parameter"]
        self.params = data["params"]


    @property
    def value(self):
        return { "type": self.key,
                 "index_parameter": self.index_parameter,
                 "params": self.params,
               }


