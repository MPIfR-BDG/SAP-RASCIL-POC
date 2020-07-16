import unittest
import importlib
import os
from pyop_api_mock import API, _Message


class BaseRascilTest(unittest.TestCase):
    def get_path(self, fname):
        return os.path.join(self._data_path, fname)

    def setUp(self):
        spec = importlib.util.spec_from_file_location(
            "script", self.get_path("script.py"))
        self.script = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.script)
        self.api = API()
        self.api.Message = _Message

    def log_config(self):
        for key, value in self.api.config.__dict__.items():
            self.api.logger.info("Config:  {} == {}".format(key, value))

    def tearDown(self):
        pass

    def pickles_to_ports(self, ports, pickle_files):
        def read(pickle_file):
            with open(pickle_file, "rb") as f:
                return f.read()
        self.api.test.write(ports, [read(i) for i in pickle_files])

