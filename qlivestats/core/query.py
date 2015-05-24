import simplejson as json

from qlivestats.core import qsocket
from qlivestats.core import config
from qlivestats.core import logger
from qlivestats.helpers import json as jsonhelp

class BaseQueryError(Exception):
    pass

class NotSupportTableError(BaseQueryError):
    pass

class NoTableSpecifiedError(BaseQueryError):
    pass

class BrokerNotSpecified(BaseQueryError):
    pass

class JSONNotWellFormedFromServer(BaseQueryError):
    pass


class Query(object):

    def __init__(self, broker=None):
        self.broker = broker if broker else config.YAMLConfig().get_broker()
        self.table = None
        self.filters = []
        self.columns = []
        
    def __getattr__(self, name):
        supportedTables = ["hosts","services","hostgroups","servicegroups",
                           "contactgroups","servicesbygroup","servicesbyhostgroup",
                           "hostsbygroup","contacts","commands","timeperiods",
                           "downtimes","comments","log","status","columns",
                           "statehist"]

        if name in supportedTables:
            self.table = name
            self.filters = []
            self.columns = []
        else:
            raise NotSupportTableError("The table you want to query does not exist.")

        return self

    def run(self):

        if not self.broker:
            raise BrokerNotSpecified("Live Status broker is not defined for the query.")    

        qs = qsocket.Socket(self.broker)
        raw_results = qs.get(str(self))

        if not raw_results:
            return []

        table = [ line.split(';') for line in raw_results.split('\n')[:-1] ] 

        # Note that first dict in the parsed object are our headers.

        ret = [] 

        for val in table[1:]:
            ret.append(dict(zip(table[0],val)))

        return ret

    def __str__(self):
        if not self.table:
            raise NoTableSpecifiedError("You have to specify a query table.")
        
        query_string = 'GET %s' % (self.table)

        # Columns
        if any(self.columns):
            query_string += "\nColumns: %s" % (' '.join(self.columns))

        # Filters
        if any(self.filters):
            for filter in self.filters:
                query_string += "\nFilter: %s" % (filter)

        # Need Headers, to know what we are working with.
        query_string += "\nColumnHeaders: on"

        # Need to end with newline
        query_string += "\n"

        return query_string

    def Filter(self, filter):
        if filter not in self.filters:
            self.filters.append(filter)
        return self

    def Column(self, column):
        columns = column.split(" ")
        for column in columns:
            if column not in self.columns:
                self.columns.append(column)
        return self

    def Columns(self, columns):
        return self.Column(columns)
