import codecs
import pickle
import os
from rascil_test_helper import BaseRascilTest


class TestVisibilitySim(BaseRascilTest):
    _data_path = os.path.dirname(__file__)

    def setUp(self):
        super(TestVisibilitySim, self).setUp()
        self.api.config.antenna_configuration = "LOWBD2"
        self.api.config.frequency_hi_hz = 120000000
        self.api.config.frequency_low_hz = 100000000
        self.api.config.max_radius = 300
        self.api.config.n_frequency_windows = 7
        self.api.config.n_time_steps = 5
        self.api.config.phasecentre_dec_deg = -60
        self.api.config.phasecentre_epoch = "J2000"
        self.api.config.phasecentre_frame = "icrs"
        self.api.config.phasecentre_ra_deg = 30

    def test_default_config(self):
        self.script.wrapper(self.api)
        self.log_config()
        self.api.test.write("input", "{}")  # empty json input

        while self.api.test.hasnext("output"):
            vis_pickle = self.api.test.read("output")
            vis_list = pickle.loads(codecs.decode(vis_pickle.encode(), "base64"))
            self.api.logger.info("{} visibilities returned".format(len(vis_list)))
            with open(self.get_path("vislist_out.pickle"), "wb") as f:
                pickle.dump(vis_list, f)
