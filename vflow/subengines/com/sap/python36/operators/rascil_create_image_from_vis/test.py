import unittest
import pickle
import importlib.util
from pyop_api_mock import API, _Message

spec = importlib.util.spec_from_file_location(
    "script", __file__.replace("test.py", "script.py"))
script = importlib.util.module_from_spec(spec)
spec.loader.exec_module(script)


class TestCreateImageFromVis(unittest.TestCase):
    def setUp(self):
        self.api = API()
        self.api.Message = _Message

    def tearDown(self):
        pass

    def test_default_config(self):
        script.wrapper(self.api)

        print('Test: Default')
        print(self.api.config)
        file = open(__file__.replace("test.py", "vislist.pickle"), "rb")
        vis_pickle = pickle.load(file)
        file.close()
        file = open(__file__.replace("test.py", "advice.pickle"), "rb")
        advice_pickle = pickle.load(file)
        file.close()
        self.api.test.write(["inputvis","inputadvice"],[pickle.dumps(vis_pickle),pickle.dumps(advice_pickle)])
        while self.api.test.hasnext("output"):
            image_pickle = self.api.test.read("output")
            image = pickle.loads(image_pickle)
            print(str(image))
