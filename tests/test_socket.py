from qlivestats.core.qsocket import Socket, SocketConnectionError
from qlivestats.core import config

from unittest import TestCase

from tests import tests_dir
os.chdir(tests_dir)

class SocketTests(TestCase):

    def __init__(self, *args, **kwargs):
        super(BasicConfigTest, self).__init__(*args, **kwargs)
        self.cfg = config.YAMLConfig(os.path.join(tests_dir, 'configtst/qlivestats.yaml'))

    def test_connect_socket(self):
        _socket = qsocket.Socket(self.cfg["livestatus"]["broker"])
        self.assertEqual(_socket.connect(),True)

    def test_failconnect_socket(self):
        _socket = qsocket.Socket("/var/lib/share/somesocketthatdoesnotexist")
        self.assertRaises(SocketConnectionError, lambda: list(_socket.connect()))




