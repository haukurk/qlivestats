from unittest import TestCase

from qlivestats.core import config

class BasicConfigTest(TestCase):

    def test_exists_config(self):
        
        qliveConfig = config.Config(name="qlivestats")
        doesItExists = qliveConfig.get_config("configtst/qlivestats.conf")

        self.assertEqual(doesItExists, True)

    def test_nonexists_config(self):
        
        qliveConfig = config.Config(name="qlivestats")
        doesItExists = qliveConfig.get_config("configtst/qlivestats.cfg")
        
        self.assertEqual(doesItExists, False)


