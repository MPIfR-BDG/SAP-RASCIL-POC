import pickle
import os
from rascil_test_helper import BaseRascilTest


class TestPredictVisibility(BaseRascilTest):
    _data_path = os.path.dirname(__file__)

    def test_default_config(self):
        self.log_config()
        self.script.wrapper(self.api)
        self.pickles_to_ports(
            ["inputvis", "inputmodel", "inputadvice"],
            [self.get_path("vislist.pickle"),
             self.get_path("gleam_model.pickle"),
             self.get_path("advice.pickle")])

        while self.api.test.hasnext("output"):
            vis_pickle = self.api.test.read("output")
            vis_list = pickle.loads(vis_pickle)
            self.api.logger.info("{} visibilities returned".format(len(vis_list)))
            with open(self.get_path("vislist_out.pickle"), "wb") as f:
                pickle.dump(vis_list, f)
