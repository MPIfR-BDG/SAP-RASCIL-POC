import os
import pickle
from rascil_test_helper import BaseRascilTest


class TestGleamModel(BaseRascilTest):
    _data_path = os.path.dirname(__file__)

    def setUp(self):
        super(TestGleamModel, self).setUp()
        self.api.config.flux_limit = 1

    def test_default_config(self):
        self.log_config()
        self.script.wrapper(self.api)
        self.pickles_to_ports(
            ["inputvis", "inputadvice"],
            [self.get_path("vislist.pickle"),
             self.get_path("advice.pickle")])

        while self.api.test.hasnext("output"):
            model_pickle = self.api.test.read("output")
            model_list = pickle.loads(model_pickle)
            self.api.logger.info("{} models returned".format(len(model_list)))
            with open(self.get_path("modellist_out.pickle"), "wb") as f:
                pickle.dump(model_list, f)
