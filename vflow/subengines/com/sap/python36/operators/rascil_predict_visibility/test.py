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


class TestPredictVisibility(unittest.TestCase):
    def setUp(self):
        self.api = API()
        self.api.Message = _Message

    def pickles_to_ports(self, ports, pickle_files):
        def read(pickle_file):
            with open(pickle_file, "rb") as f:
                return f.read()
        self.api.test.write(ports, [read(i) for i in pickle_files])

    def test_default_config(self):
        print('Test: Default')
        print(self.api.config)
        script.wrapper(self.api)
        print(self.api.callbacks.items())
        self.pickles_to_ports(
            ["inputvis", "inputmodel", "inputadvice"],
            [get_path("vislist.pickle"),
             get_path("gleam_model.pickle"),
             get_path("advice.pickle")])

        while self.api.test.hasnext("output"):
            vis_pickle = self.api.test.read("output")
            vis_list = pickle.loads(vis_pickle)
            print(str(len(vis_list)))
            print(str(vis_list))
            for vis in vis_list:
                print(str(vis))
            with open(get_path("vislist_out.pickle"), "wb") as f:
                pickle.dump(vis_list, f)
