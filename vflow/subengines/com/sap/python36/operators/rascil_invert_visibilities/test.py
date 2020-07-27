import pickle
import codecs
import os
from rascil_test_helper import BaseRascilTest


class TestInvertVisibilities(BaseRascilTest):
    _data_path = os.path.dirname(__file__)

    def setUp(self):
        super(TestInvertVisibilities, self).setUp()
        self.api.config.dopsf = False

    def _test_helper(self, dopsf, outfile):
        self.api.config.dopsf = dopsf
        self.log_config()
        self.script.wrapper(self.api)
        self.text_pickles_to_ports(
            ["inputmodel", "inputvis", "inputadvice"],
            [self.get_path("model_list.pickle.txt"),
             self.get_path("vislist.pickle.txt"),
             self.get_path("advice.pickle.txt")])

        while self.api.test.hasnext("output"):
            image_pickle = self.api.test.read("output")
            image_list = pickle.loads(codecs.decode(image_pickle.encode(), "base64"))
            self.api.logger.info("Generated {} images".format(len(image_list)))
            with open(self.get_path(outfile), "wb") as f:
                pickle.dump(image_list, f)

    def test_dopsf_false(self):
        self._test_helper(False, "imagelist_out.pickle")

    def test_dopsf_true(self):
        self._test_helper(True, "psflist_out.pickle")
