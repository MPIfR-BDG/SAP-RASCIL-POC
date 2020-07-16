import unittest
import pickle
import importlib.util
from pyop_api_mock import API, _Message

spec = importlib.util.spec_from_file_location(
    "script", __file__.replace("test.py", "script.py"))
script = importlib.util.module_from_spec(spec)
spec.loader.exec_module(script)


class TestCorruptVis(unittest.TestCase):
    def setUp(self):
        self.api = API()
        self.api.Message = _Message
        self.api.config.phase_error = 1

    def tearDown(self):
        pass

    def test_default_config(self):
        script.wrapper(self.api)

        print('Test: Default')
        print(self.api.config)
        file = open(__file__.replace("test.py", "predicted_vislist.pickle"), "rb")
        predicted_vislist_pickle = pickle.load(file)
        file.close()
        self.api.test.write("input",pickle.dumps(predicted_vislist_pickle))
        while self.api.test.hasnext("output"):
            corrupted_vislist_pickle = self.api.test.read("output")
            corrupted_vislist = pickle.loads(corrupted_vislist_pickle)
            print(str(corrupted_vislist))
