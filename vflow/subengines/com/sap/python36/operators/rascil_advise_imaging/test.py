import unittest
import pickle
import importlib.util
from pyop_api_mock import API, _Message

spec = importlib.util.spec_from_file_location(
    "script", __file__.replace("test.py", "script.py"))
script = importlib.util.module_from_spec(spec)
spec.loader.exec_module(script)


class TestAdviceImaging(unittest.TestCase):
    def setUp(self):
        self.api = API()
        self.api.Message = _Message
        self.api.config.delA = 0.02
        self.api.config.guard_band_image = 8
        self.api.config.wprojection_planes = 1

    def tearDown(self):
        pass

    def test_default_config(self):
        script.wrapper(self.api)

        print('Test: Default')
        print(self.api.config)
        file = open(__file__.replace("test.py", "vislist.pickle"), "rb")
        vis_pickle = pickle.load(file)
        file.close()
        self.api.test.write("input",pickle.dumps(vis_pickle))
        while self.api.test.hasnext("output"):
            advice_pickle = self.api.test.read("output")
            advice = pickle.loads(advice_pickle)
            print(str(advice))
