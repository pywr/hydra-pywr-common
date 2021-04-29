from hydra_pywr_common.types.base import(
    PywrDataReference
)

from .base import Fragment

class Timestepper(Fragment):
    def __init__(self, data):
        super().__init__()

        """
        self._start = datetime.datetime.fromisoformat(data["start"])
        self._end = datetime.datetime.fromisoformat(data["end"])
        self._timestep = int(data["timestep"])   # int only ???
        """

        self._start = PywrDataReference.ReferenceFactory("start", data["start"])
        self._end = PywrDataReference.ReferenceFactory("end", data["end"])
        self._timestep = PywrDataReference.ReferenceFactory("timestep", data["timestep"])

        @property
        def start(self):
            return self._start

        @property
        def end(self):
            return self._end

        @property
        def timestep(self):
            return self._timestep


class Metadata(Fragment):
    def __init__(self, data):
        super().__init__()

        self.title = PywrDataReference.ReferenceFactory("title", data["title"])
        self.description = PywrDataReference.ReferenceFactory("description", data["description"]) if data.get("description") else ""
