import unittest
import pickle
import importlib.util
from pyop_api_mock import API, _Message


def get_path(file):
    return __file__.replace("test.py", file)


spec = importlib.util.spec_from_file_location(
    "script", get_path("script.py"))
script = importlib.util.module_from_spec(spec)
spec.loader.exec_module(script)


class TestGleamModel(unittest.TestCase):
    def setUp(self):
        self.api = API()
        self.api.Message = _Message
        self.api.config.flux_limit = 1

    def pickles_to_ports(self, ports, pickle_files):
        def read(pickle_file):
            with open(pickle_file, "rb") as f:
                return f.read()
        self.api.test.write(ports, [read(i) for i in pickle_files])

    def test_default_config(self):
        print('Test: Default')
        print(self.api.config)
        script.wrapper(self.api)
        self.pickles_to_ports(
            ["inputvis", "inputadvice"],
            [get_path("vislist.pickle"),
             get_path("advice.pickle")])

        while self.api.test.hasnext("output"):
            model_pickle = self.api.test.read("output")
            model_list = pickle.loads(model_pickle)
            print(str(len(model_list)))
            print(str(model_list))
            for model in model_list:
                print(str(model))
            with open(get_path("modellist_out.pickle"), "wb") as f:
                pickle.dump(model_list, f)
