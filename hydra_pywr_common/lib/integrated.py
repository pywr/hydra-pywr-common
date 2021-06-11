import json
from .readers import PywrJsonReader
from hydra_pywr_common.types.network import PywrNetwork


class PywrIntegratedNetwork():
    def __init__(self, filename):
        with open(filename, 'r') as fp:
            self.src = json.load(fp)

        self.build_networks_and_config()

    def build_networks_and_config(self):
        water_src = self.src["water_network"]
        self.water = PywrNetwork.from_source_json(water_src)

        energy_src = self.src["energy_network"]
        self.energy = PywrNetwork.from_source_json(energy_src)

        self.config = self.src["config"]
