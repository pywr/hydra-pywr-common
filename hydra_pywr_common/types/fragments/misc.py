from .base import Fragment

class PywrBathymetry(Fragment):
    key = "bathymetry"

    def __init__(self, data):
        super().__init__()


class PywrWeather(Fragment):
    key = "weather"

    def __init__(self, data):
        super().__init__()

class NodeList(Fragment):
    def __init__(self, data):
        super().__init__()
