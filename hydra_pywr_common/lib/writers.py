import json

from hydra_pywr_common.types.base import(
    PywrNode,
    PywrParameter,
    PywrRecorder,
    PywrEdge
)

from hydra_pywr_common.lib.utils import(
    parse_reference_key
)

from hydra_pywr_common.types.fragments.network import(
    Timestepper,
    Metadata
)

class PywrJsonWriter():

    def __init__(self, network):
        self.network = network
        self.output = {}

    def as_json(self):
        self.output["timestepper"] = self.process_timestepper()
        self.output["metadata"] = self.process_metadata()
        #self.output["parameters"] = self.process_parameters()
        self.output["recorders"] = self.process_recorders()

        return json.dumps(self.output)


    def process_timestepper(self):
        timestepper = self.network.timestepper
        return { "start": timestepper.start,
                 "end": timestepper.end,
                 "timestep": timestepper.timestep
               }

    def process_metadata(self):
        metadata = self.network.metadata
        return { "title": metadata.title,
                 "description": metadata.description
               }

    def process_parameters(self):
        parameters = self.network.parameters

        return { ref: param.value for ref, param in parameters.items() }

    def process_recorders(self):
        recorders = self.network.recorders

        return { ref: rec.value for ref, rec in recorders.items() }
