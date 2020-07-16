import unittest
import pickle
import importlib.util
from pyop_api_mock import API, _Message

spec = importlib.util.spec_from_file_location(
    "script", __file__.replace("test.py", "script.py"))
script = importlib.util.module_from_spec(spec)
spec.loader.exec_module(script)


class TestVisibilitySim(unittest.TestCase):
    def setUp(self):
        self.api = API()
        self.api.Message = _Message
        self.api.config.antenna_configuration = "LOWBD2"
        self.api.config.frequency_hi_hz = 120000000
        self.api.config.frequency_low_hz = 100000000
        self.api.config.max_radius = 300
        self.api.config.n_frequency_windows = 7
        self.api.config.n_time_steps = 5
        self.api.config.phasecentre_dec_deg = -60
        self.api.config.phasecentre_epoch = "J2000"
        self.api.config.phasecentre_frame = "icrs"
        self.api.config.phasecentre_ra_deg = 30

    def tearDown(self):
        pass

    def test_default_config(self):
        script.wrapper(self.api)

        print('Test: Default')
        print(self.api.config)
        self.api.test.write("input", "{}")  # empty json input
        while self.api.test.hasnext("output"):
            vis_pickle = self.api.test.read("output")
            vis_list = pickle.loads(vis_pickle)
            print(str(len(vis_list)))
            print(str(vis_list))
            for vis in vis_list:
                print(str(vis))
            pickle_file = open("vislist.pickle", "wb")
            pickle.dump(vis_list, pickle_file)
            pickle_file.close()