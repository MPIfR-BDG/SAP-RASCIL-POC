import pickle
import os
from rascil_test_helper import BaseRascilTest


class TestCorruptVis(BaseRascilTest):
    _data_path = os.path.dirname(__file__)

    def setUp(self):
        super(TestCorruptVis, self).setUp()
        self.api.config.phase_error = 1

    def test_default_config(self):
        self.script.wrapper(self.api)
        self.log_config()
        self.pickles_to_ports(
            ["input", ], [self.get_path("predicted_vislist.pickle"), ])

        while self.api.test.hasnext("output"):
            corrupted_vislist_pickle = self.api.test.read("output")
            corrupted_vislist = pickle.loads(corrupted_vislist_pickle)
            self.api.logger.info("{} corrupted visibilities returned".format(
                len(corrupted_vislist)))
