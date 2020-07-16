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


class TestDeconvolve(unittest.TestCase):
    def setUp(self):
        self.api = API()
        self.api.Message = _Message
        self.api.config.flux_limit = 1
        self.api.config.algorithm = "msclean",
        self.api.config.deconvolve_facets = 8,
        self.api.config.deconvolve_overlap = 16,
        self.api.config.deconvolve_taper = "tukey",
        self.api.config.fractional_threshold = 0,
        self.api.config.gain = 0,
        self.api.config.niter = 1000,
        self.api.config.psf_support = 64,
        self.api.config.scales = [0, 3, 10],
        self.api.config.threshold = 0

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
            ["inputimage", "inputpsf", "inputmodel"],
            [get_path("imagelist.pickle"),
             get_path("psflist.pickle"),
             get_path("modellist.pickle")])

        while self.api.test.hasnext("output"):
            image_pickle = self.api.test.read("output")
            image_list = pickle.loads(image_pickle)
            print(str(len(image_list)))
            print(str(image_list))
            for image in image_list:
                print(str(image))
            with open(get_path("imagelist_out.pickle"), "wb") as f:
                pickle.dump(image_list, f)
