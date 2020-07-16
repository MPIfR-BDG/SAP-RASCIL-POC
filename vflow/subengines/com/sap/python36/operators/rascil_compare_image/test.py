import unittest
import pickle
import importlib.util
from pyop_api_mock import API, _Message

spec = importlib.util.spec_from_file_location(
    "script", __file__.replace("test.py", "script.py"))
script = importlib.util.module_from_spec(spec)
spec.loader.exec_module(script)


class TestCompareImage(unittest.TestCase):
    def setUp(self):
        self.api = API()
        self.api.Message = _Message

    def tearDown(self):
        pass

    def test_default_config(self):
        script.wrapper(self.api)

        print('Test: Default')
        print(self.api.config)

        file_image1 = open(__file__.replace("test.py", "test_image1.pickle"), "rb")
        image1_pickle = pickle.load(file_image1)
        file_image1.close()

        file_image2 = open(__file__.replace("test.py", "test_image2.pickle"), "rb")
        image2_pickle = pickle.load(file_image2)
        file_image2.close()

        self.api.test.write(["image1","image2"],(pickle.dumps(image1_pickle),pickle.dumps(image2_pickle)))

        while self.api.test.hasnext("output"):
            comp_pickle = self.api.test.read("output")
            comp = pickle.loads(comp_pickle)
            print(str(comp))
