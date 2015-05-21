from qlivestats.core import config
from qlivestats.core.query import Query, NotSupportTableError, BrokerNotSpecified
from qlivestats.core.qsocket import Socket

from unittest import TestCase
import mock
import os
from tests import tests_dir
os.chdir(tests_dir)

class QueryTests(TestCase):

    def __init__(self, *args, **kwargs):
        super(QueryTests, self).__init__(*args, **kwargs)
        self.cfg = config.YAMLConfig(os.path.join(tests_dir, 'configtst/qlivestats.yaml'))
        self._q = Query(self.cfg.get_broker())
            
    def test_query_hosts_with_no_filters(self):
        self.assertEqual(str(self._q.hosts), "GET hosts\n")

    def test_query_services_with_no_filters(self):
        self.assertEqual(str(self._q.services), "GET services\n")

    def test_query_logs(self):
        self.assertEqual(str(self._q.log), "GET log\n")

    def test_query_hosts_specific_columns(self):
        self._q.hosts.Column("host_name") \
        .Column("description") \
        .Column("state")

        self.assertEqual(str(self._q), "GET hosts\nColumns: host_name "
                         "description state\n")

    def test_query_services_filter(self):
        query = self._q.services.Filter("state = 2")

        self.assertEqual(str(query), "GET services\nFilter: state = 2\n")

    def test_query_services_multiple_filters(self):
        query = self._q.services \
        .Filter("state = 2") \
        .Filter("in_notification_period = 1")

        self.assertEqual(str(query), "GET services\nFilter: state = 2\n"
                         "Filter: in_notification_period = 1\n")

    def test_bad_table(self):
        self.assertRaises(NotSupportTableError, lambda: list(self._q.somebadtable))

    def test_trying_to_load_default_config_that_does_not_have_broker_defined(self):
        with mock.patch('qlivestats.core.config.YAMLConfig') as MockClass:
            confInst = MockClass.return_value
            confInst.get_broker.return_value = None
            query = Query()
            self.assertRaises(BrokerNotSpecified, lambda: list(query.services.run()))

    def test_bad_config_when_getting_default(self):
        self.assertRaises(config.ConfigReadError, lambda: list(Query()))

    def test_run_query(self):
        with mock.patch('qlivestats.core.qsocket.socket.socket') as socketmock:
            socketmock.return_value.recv.return_value = "Not important"
            socketmock.return_value.connect.return_value = ''
            res = self._q.services.run()
            self.assertEqual(res,'Not important')



