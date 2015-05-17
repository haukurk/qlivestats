from qlivestats.core.qsocket import Socket, SocketConnectionError 
from qlivestats.core import config

from unittest import TestCase
import os
from tests import tests_dir
os.chdir(tests_dir)

class SocketTests(TestCase):

    def __init__(self, *args, **kwargs):
        super(SocketTests, self).__init__(*args, **kwargs)
        self.cfg = config.YAMLConfig(os.path.join(tests_dir, 'configtst/qlivestats.yaml'))

    #def setUp(self):
        #super(SocketTests, self).setUp()
        #self.mox = mox.Mox()
        #self.mock_socket = self.mox.CreateMockAnything(socket.socket)
        #self.mox.StubOutWithMock(socket, 'getservbyname')
        #self.mox.StubOutWithMock(socket, 'socket')
        #socket.socket(socket.AF_INET, socket.SOCK_STREAM).AndReturn(self.mock_socket)


    #def test_connect_socket(self):
        #_socket = Socket(self.cfg)
        #self.assertEqual(_socket.connect(),True)

    def test_failconnect_socket(self):
        _socket = Socket(self.cfg)
        self.assertRaises(SocketConnectionError, lambda: list(_socket.connect()))




