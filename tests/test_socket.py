from qlivestats.core.qsocket import Socket, SocketConnectionError 
from qlivestats.core import config

from mock import patch

from unittest import TestCase
import os
from tests import tests_dir
os.chdir(tests_dir)

class SocketTests(TestCase):

    def __init__(self, *args, **kwargs):
        super(SocketTests, self).__init__(*args, **kwargs)
        self.cfg = config.YAMLConfig(os.path.join(tests_dir, 
                                                  'configtst/qlivestats.yaml'))

    @patch('qlivestats.core.qsocket.socket.socket')
    def test_connect_socket(self, qsmock):

        expValue = (
                        'acknowledged;action_url;address;alias;check_command;check_period;'
                        'checks_enabled;contacts;in_check_period;in_notification_period;'
                        'is_flapping;last_check;last_state_change;name;notes;notes_url;'
                        'notification_period;scheduled_downtime_depth;state;total_services'
                        '0;/nagios/pnp/index.php?host=$HOSTNAME$;127.0.0.1;Acht;check-mk-ping;;1;che'
                        'ck_mk,hh;1;1;0;1256194120;1255301430;Acht;;;24X7;0;0;7'
                        '0;/nagios/pnp/index.php?host=$HOSTNAME$;127.0.0.1;DREI;check-mk-ping;;1;che'
                        'ck_mk,hh;1;1;0;1256194120;1255301431;DREI;;;24X7;0;0;1'
                        '0;/nagios/pnp/index.php?host=$HOSTNAME$;127.0.0.1;Drei;check-mk-ping;;1;che'
                        'ck_mk,hh;1;1;0;1256194120;1255301435;Drei;;;24X7;0;0;4'
                    )

        qsmock.return_value.recv.return_value = expValue 
        qsmock.return_value.connect.return_value = ''
        
        _socket = Socket(self.cfg)

        results = _socket.get("get hosts\n")

        self.assertEqual(results,
                         expValue 
                         )

    def test_failconnect_socket(self):
        _socket = Socket(self.cfg)
        self.assertRaises(SocketConnectionError, lambda: list(_socket.connect()))




