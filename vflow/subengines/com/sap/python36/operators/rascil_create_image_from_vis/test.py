import pickle
import os
from rascil_test_helper import BaseRascilTest


class TestCreateImageFromVis(BaseRascilTest):
    _data_path = os.path.dirname(__file__)

    def test_default_config(self):
        self.script.wrapper(self.api)
        self.log_config()
        self.pickles_to_ports(
            ["inputvis", "inputadvice"],
            [self.get_path("vislist.pickle"),
             self.get_path("advice.pickle")])

        while self.api.test.hasnext("output"):
            image_pickle = self.api.test.read("output")
            image_list = pickle.loads(image_pickle)
            self.api.logger.info("{} image templates returned".format(
                len(image_list)))
