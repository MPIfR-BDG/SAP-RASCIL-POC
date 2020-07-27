import pickle
import codecs
import os
from rascil_test_helper import BaseRascilTest


class TestAdviseImaging(BaseRascilTest):
    _data_path = os.path.dirname(__file__)

    def setUp(self):
        super(TestAdviseImaging, self).setUp()
        self.api.config.delA = 0.02
        self.api.config.guard_band_image = 8
        self.api.config.wprojection_planes = 1

    def test_default_config(self):
        self.script.wrapper(self.api)
        self.log_config()
        self.text_pickles_to_ports(
            ["input"], [self.get_path("vislist.pickle.txt")])

        while self.api.test.hasnext("output"):
            advice_pickle = self.api.test.read("output")
            advice = pickle.loads(codecs.decode(advice_pickle.encode(), "base64"))
            self.api.logger.info("Imaging advice: {}".format(advice))
