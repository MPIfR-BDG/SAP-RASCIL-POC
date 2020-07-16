import unittest
import pickle
import importlib.util
from pyop_api_mock import API, _Message

spec = importlib.util.spec_from_file_location(
    "script", __file__.replace("test.py", "script.py"))
script = importlib.util.module_from_spec(spec)
spec.loader.exec_module(script)


def get_path(file):
    return __file__.replace("test.py", file)


class TestGleamModel(unittest.TestCase):
    def setUp(self):
        self.api = API()
        self.api.Message = _Message
        self.api.config.flux_limit = 1

    def pickle_to_port(self, port, pickle_file):
        with open(pickle_file, "rb") as f:
            self.api.test.write("port", f.read())

    def test_default_config(self):
        print('Test: Default')
        print(self.api.config)
        script.wrapper(self.api)
        self.pickle_to_port("inputvis", get_path("vislist.pickle"))
        self.pickle_to_port("inputadvice", get_path("advice.pickle"))

        while self.api.test.hasnext("output"):
            model_pickle = self.api.test.read("output")
            model_list = pickle.loads(model_pickle)
            print(str(len(model_list)))
            print(str(model_list))
            for model in model_list:
                print(str(model))
            with open(get_path("modellist_out.pickle"), "wb") as f:
                pickle.dump(model_list, f)
