from qlivestats.core import config
from qlivestats.core.query import Query, NotSupportTableError
from qlivestats.core.qsocket import Socket

from unittest import TestCase
from mock import Mock
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
