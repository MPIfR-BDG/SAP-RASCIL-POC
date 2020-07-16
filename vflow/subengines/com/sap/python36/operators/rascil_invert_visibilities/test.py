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


class TestInvertVisibilities(unittest.TestCase):
    def setUp(self):
        self.api = API()
        self.api.Message = _Message
        self.api.config.dopsf = False

    def pickles_to_ports(self, ports, pickle_files):
        def read(pickle_file):
            with open(pickle_file, "rb") as f:
                return f.read()
        self.api.test.write(ports, [read(i) for i in pickle_files])

    def _test_helper(self, dopsf, outfile):
        self.api.config.dopsf = dopsf
        print(self.api.config)
        script.wrapper(self.api)
        self.pickles_to_ports(
            ["inputmodel", "inputvis", "inputadvice"],
            [get_path("modellist.pickle"),
             get_path("vislist.pickle"),
             get_path("advice.pickle")])

        while self.api.test.hasnext("output"):
            image_pickle = self.api.test.read("output")
            image_list = pickle.loads(image_pickle)
            print(str(len(image_list)))
            print(str(image_list))
            for image in image_list:
                print(str(image))
            with open(get_path(outfile), "wb") as f:
                pickle.dump(image_list, f)

    def test_dopsf_false(self):
        print('Test: dopsf false')
        self._test_helper(False, "imagelist_out.pickle")

    def test_dopsf_true(self):
        print('Test: dopsf true')
        self._test_helper(True, "psflist_out.pickle")
