from qlivestats.core import qsocket
from qlivestats.core import config

class BaseQueryError(Exception):
    pass

class NotSupportTableError(BaseQueryError):
    pass

class NoTableSpecifiedError(BaseQueryError):
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
        else:
            raise NotSupportTableError("The table you want to query does not exist.")

        return self

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

        return query_string + "\n"

    def Filter(self, filter):
        if filter not in self.filters:
            self.filters.append(filter)
        return self

    def Column(self, column):
        if column not in self.columns:
            self.columns.append(column)
        return self
