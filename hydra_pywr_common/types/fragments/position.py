from .base import Fragment


class Coordinate():
    coordinate_type_map = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Coordinate.coordinate_type_map[cls.key] = cls

    @staticmethod
    def CoordinateFactory(data):
        instkey = next(iter(data))
        instcls = Coordinate.coordinate_type_map[instkey]
        return instcls(*data[instkey])


class GeographicCoordinate(Coordinate):
    key = "geographic"
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

    @property
    def value(self):
        return { self.key: [ self.x, self.y ] }


class SchematicCoordinate(Coordinate):
    key = "schematic"
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

    @property
    def value(self):
        return { self.key: [ self.x, self.y ] }


class PywrPosition(Fragment):
    key = "position"

    def __init__(self, data):
        super().__init__()
        self.coordinates = []

        for key, data in data.items():
            c = Coordinate.CoordinateFactory({key: data})
            self.coordinates.append(c)

    @property
    def value(self):
        val = {}
        #val = { c.key: c.value for c in self.coordinates }
        for c in self.coordinates:
            val.update(c.value)
        return val
