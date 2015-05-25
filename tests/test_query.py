from qlivestats.core import config
from qlivestats.core.query import Query, NotSupportTableError, BrokerNotSpecified, NoTableSpecifiedError 
from qlivestats.core.qsocket import Socket

from unittest import TestCase
import mock
import logging
import os
import sys
from tests import tests_dir
os.chdir(tests_dir)

class QueryTests(TestCase):

    def __init__(self, *args, **kwargs):
        super(QueryTests, self).__init__(*args, **kwargs)
        self.cfg = config.YAMLConfig(os.path.join(tests_dir, 'configtst/qlivestats.yaml'))
        self._q = Query(self.cfg.get_broker())
        logging.basicConfig( stream=sys.stderr )
        logging.getLogger( "TestQLiveStats" ).setLevel( logging.DEBUG )

    def test_query_hosts_with_no_filters(self):
        self.assertEqual(str(self._q.hosts), "GET hosts\nColumnHeaders: on\n")

    def test_query_hosts_with_reset_filters(self):
        self.assertEqual(str(self._q.hosts.Columns("host name")),"GET hosts\nColumns: host name\nColumnHeaders: on\n")
        self.assertEqual(str(self._q.hosts), "GET hosts\nColumnHeaders: on\n")

    def test_query_services_with_no_filters(self):
        self.assertEqual(str(self._q.services), "GET services\nColumnHeaders: on\n")

    def test_query_logs(self):
        self.assertEqual(str(self._q.log), "GET log\nColumnHeaders: on\n")

    def test_query_hosts_specific_columns(self):
        self._q.hosts.Column("host_name") \
        .Column("description") \
        .Column("state")

        self.assertEqual(str(self._q), "GET hosts\nColumns: host_name "
                         "description state\nColumnHeaders: on\n")

    def test_query_services_filter(self):
        query = self._q.services.Filter("state = 2")

        self.assertEqual(str(query), "GET services\nFilter: state = 2\nColumnHeaders: on\n")

    def test_query_services_multiple_filters(self):
        query = self._q.services \
        .Filter("state = 2") \
        .Filter("in_notification_period = 1")

        self.assertEqual(str(query), "GET services\nFilter: state = 2\n"
                         "Filter: in_notification_period = 1\nColumnHeaders: on\n")

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

    def test_run_query_parse_csv(self):
        with mock.patch('qlivestats.core.qsocket.socket.socket') as socketmock:
            socketmock.return_value.recv.return_value = 'accept_passive_checks;acknowledged;acknowledgement_type\n1;1;1\n2;2;2'
            socketmock.return_value.connect.return_value = ''
            res = self._q.hosts.run()
            self.assertEqual(res, [
                {"accept_passive_checks": "1","acknowledged": "1","acknowledgement_type": "1"},
                {"accept_passive_checks": "2","acknowledged": "2","acknowledgement_type": "2"}
            ])

    def test_run_query_parse_csv_single(self):
        with mock.patch('qlivestats.core.qsocket.socket.socket') as socketmock:
            socketmock.return_value.recv.return_value = 'accept_passive_checks;acknowledged;acknowledgement_type\n1;1;1'
            socketmock.return_value.connect.return_value = ''
            res = self._q.hosts.run()
            self.assertEqual(res, [
                {"accept_passive_checks": "1","acknowledged": "1","acknowledgement_type": "1"}
            ])

    def test_run_query_parse_csv_fail(self):
         with mock.patch('qlivestats.core.qsocket.socket.socket') as socketmock:
            socketmock.return_value.recv.return_value = 'accept_passive_checks;acknowledged;acknowledgement_type\n1;1;1'
            socketmock.return_value.connect.return_value = ''
            res = self._q.hosts.run()
            self.assertNotEqual(res, [
                {"accept_passive_checks": "0","acknowledged": "1","acknowledgement_type": "1"}
            ])

    def test_describe_table(self):
         with mock.patch('qlivestats.core.qsocket.socket.socket') as socketmock:
            socketmock.return_value.recv.return_value = 'accept_passive_checks;acknowledged;acknowledgement_type'
            socketmock.return_value.connect.return_value = ''
            res = self._q.hosts.Describe()
            self.assertEqual(res, [
                "accept_passive_checks","acknowledged","acknowledgement_type"
            ])

    def tests_query_on_no_table(self):
        self.assertRaises(NoTableSpecifiedError, lambda: list(self._q.run()))
