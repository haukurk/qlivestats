import click
import pprint
from tabulate import tabulate
from qlivestats.core.query import Query
from qlivestats.core import config as configmod

def getSupportedTables():
    return ["hosts","services","hostgroups","servicegroups",
            "contactgroups","servicesbygroup","servicesbyhostgroup",
            "hostsbygroup","contacts","commands","timeperiods",
            "downtimes","comments","log","status","columns",
            "statehist"]

@click.command()
@click.option('--config', default="/etc/qlivestats.yaml", help='Config File Location')
@click.option('--table', prompt='Table to query from',
              help='Table can include hosts, services, contacts etc.')
@click.option('--filters', default="", prompt='filters for you query',
              help='Multiple filters are seperated with a comma.'
              'Please see the README for information about operators.')
@click.option('--columns', default="", prompt='columns to include in the query.',
              help='columns are seperated by a comma.')
def qlivestatsquery(config, table, filters, columns):
    """Construct a query and output the results."""
    
    # Create a Query object
    cfg = configmod.YAMLConfig(config)
    query = Query(cfg.get_broker())

    query = getattr(query, table)

    # Construct the query.
    if table not in getSupportedTables():
        raise click.BadParameter('You need to specify a table that is supported by Live Status.'
                                 '', param_hint=['--table']) 

    if filters:
        for filter in filters.split(","):
            query = query.Filter(filter)
    
    if columns:
        cols = columns.replace(","," ")
        query = query.Columns(cols) 
    else:
        click.pause(info="\n[INFO] Selecting all columns from tables can create unreadable output."
                    "\n       It's recommeded to select the columns you are interested in."
                    "\n       You can see possible columns by using qlivestat-describe [table]"
                    "\n       [ Press any key if you want to continue! ]", err=False)
    res = query.run()

    click.echo(tabulate(res, tablefmt="rst", numalign="right", headers="keys"))

@click.command()
@click.option('--config', default="/etc/qlivestats.yaml", help='Config File Location')
@click.option('--table', prompt='Table to query from',
                            help='Table can include hosts, services, contacts etc.')
def qlivestatsdescribe(config, table):
    """ Describe a table in Live Status broker"""

    # Construct the query.
    if table not in getSupportedTables():
        raise click.BadParameter('You need to specify a table that is supported by Live Status.'
                                 '', param_hint=['--table']) 

    # Create a Query object
    cfg = configmod.YAMLConfig(config)
    query = Query(cfg.get_broker())

    query = getattr(query, table)

    res = query.Describe()

    click.echo(pprint.pprint(res))
