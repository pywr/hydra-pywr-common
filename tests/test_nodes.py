from pywr.model import Model
from hydra_pywr_common.hydropower_nodes import *
import os


TEST_DIR = os.path.dirname(__file__)

def test_hydropower_model():

    m = Model.load(os.path.join(TEST_DIR, 'hydropower.json'))
    m.run()


