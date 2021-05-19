from collections import namedtuple

from .base import Fragment

try:
    """ Py>=3.7 required for default kwargs to namedtuple """
    Coord = namedtuple("Coord", ('x', 'y'), defaults=(0.0, 0.0))
except TypeError:
    Coord = namedtuple("Coord", ('x', 'y'))


class PywrPosition(Fragment):
    key = "position"
    position_type_map = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        PywrPosition.position_type_map[cls.key] = cls

    @staticmethod
    def PywrPositionFactory(data):
        instkey = next(iter(data))
        instcls = PywrPosition.position_type_map[instkey]
        return instcls(data[instkey])


class PywrGeographicPosition(PywrPosition):
    key = "geographic"

    def __init__(self, data):
        super().__init__()
        self.coord = Coord(*data)

    @property
    def y(self):
        return self.coord.y

    @property
    def x(self):
        return self.coord.x

    @property
    def value(self):
        return { self.key: [ self.x, self.y ] }
