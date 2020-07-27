import pickle
import codecs
import os
from rascil_test_helper import BaseRascilTest


class TestCompareImage(BaseRascilTest):
    _data_path = os.path.dirname(__file__)

    def test_default_config(self):
        self.script.wrapper(self.api)
        self.log_config()

        self.text_pickles_to_ports(
            ["image1", "image2"],
            [self.get_path("test_image1.pickle.txt"),
             self.get_path("test_image2.pickle.txt")])

        while self.api.test.hasnext("output"):
            comp_pickle = self.api.test.read("output")
            comp = pickle.loads(codecs.decode(comp_pickle.encode(), "base64"))
            self.api.logger.info("Image comparison {}".format(comp))
