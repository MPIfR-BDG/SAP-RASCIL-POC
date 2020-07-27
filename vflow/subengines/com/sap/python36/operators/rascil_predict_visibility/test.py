import pickle
import codecs
import os
from rascil_test_helper import BaseRascilTest


class TestPredictVisibility(BaseRascilTest):
    _data_path = os.path.dirname(__file__)

    def test_default_config(self):
        self.log_config()
        self.script.wrapper(self.api)
        self.text_pickles_to_ports(
            ["inputvis", "inputmodel", "inputadvice"],
            [self.get_path("vislist.pickle.txt"),
             self.get_path("gleam_model.pickle.txt"),
             self.get_path("advice.pickle.txt")])

        while self.api.test.hasnext("output"):
            vis_pickle = self.api.test.read("output")
            vis_list = pickle.loads(codecs.decode(vis_pickle.encode(), "base64"))
            self.api.logger.info("{} visibilities returned".format(len(vis_list)))
            with open(self.get_path("vislist_out.pickle"), "wb") as f:
                pickle.dump(vis_list, f)
