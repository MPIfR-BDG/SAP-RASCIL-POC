import os
import pickle
import codecs
from rascil_test_helper import BaseRascilTest


class TestDeconvolve(BaseRascilTest):
    _data_path = os.path.dirname(__file__)

    def setUp(self):
        super(TestDeconvolve, self).setUp()
        self.api.config.flux_limit = 1
        self.api.config.algorithm = "msclean"
        self.api.config.deconvolve_facets = 8
        self.api.config.deconvolve_overlap = 16
        self.api.config.deconvolve_taper = "tukey"
        self.api.config.fractional_threshold = 0.5
        self.api.config.gain = 1.0
        self.api.config.niter = 1000
        self.api.config.psf_support = 64
        self.api.config.scales = [0, 3, 10]
        self.api.config.threshold = 0.5

    def test_default_config(self):
        self.log_config()
        self.script.wrapper(self.api)
        self.text_pickles_to_ports(
            ["inputimage", "inputpsf", "inputmodel"],
            [self.get_path("image_list.pickle.txt"),
             self.get_path("psf_list.pickle.txt"),
             self.get_path("model_list.pickle.txt")])

        while self.api.test.hasnext("output"):
            image_pickle = self.api.test.read("output")
            image_list = pickle.loads(codecs.decode(image_pickle.encode(), "base64"))
            self.api.logger.info("{} images returned".format(len(image_list)))
            with open(self.get_path("imagelist_out.pickle"), "wb") as f:
                pickle.dump(image_list, f)
