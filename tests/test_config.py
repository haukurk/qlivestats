import os
import yaml

from unittest import TestCase

from qlivestats.core import config

from tests import tests_dir
os.chdir(tests_dir)

class BasicConfigTest(TestCase):

    def __init__(self, *args, **kwargs):
        super(BasicConfigTest, self).__init__(*args, **kwargs)

    def test_read_and_validation_config(self):
        config.YAMLConfig(os.path.join(tests_dir, 'configtst/qlivestats.yaml'))

    def test_fail_read_config(self):
        self.assertRaises(config.ConfigReadError, lambda: list(config.YAMLConfig(os.path.join(tests_dir, 'configtst/qlivestats.cfg'))))    

    def test_bad_config(self):
        self.assertRaises(config.ConfigParsingError, lambda: list(config.YAMLConfig(os.path.join(tests_dir, 'configtst/qlivestatsbad.yaml')).config))    

    def test_parsed_information(self):
        cfg = config.YAMLConfig(os.path.join(tests_dir, 'configtst/qlivestats.yaml'))
        socket = cfg.config["livestatus"]["broker"]
        self.assertEqual(socket, "/usr/share/broker/livestatus") 

    def test_tostring(self):
        cfg = config.YAMLConfig(os.path.join(tests_dir, 'configtst/qlivestats.yaml'))
        self.assertEqual(yaml.dump(cfg.config),str(cfg))

    def test_representation(self):
        cfg = config.YAMLConfig(os.path.join(tests_dir, 'configtst/qlivestats.yaml'))
        self.assertEqual("YAMLConfig (sections: 2)", cfg.__repr__())

    def test_get_filename(self):
        cfg = config.YAMLConfig(os.path.join(tests_dir, 'configtst/qlivestats.yaml'))
        self.assertEqual(cfg.get_filename(),os.path.join(tests_dir, 'configtst/qlivestats.yaml'))
