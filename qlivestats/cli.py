import click
from qlivestats.core.query import Query
from qlivestats.core import config as configmod


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
    
    if filters:
        for filter in filters.split(","):
            query = query.Filter(filter)
    
    if columns:
        cols = columns.replace(","," ")
        query = query.Columns(cols)

    res = query.run()

    click.echo(res)

@click.command()
@click.option('--config', default="/etc/qlivestats.yaml", help='Config File Location')
@click.option('--table', prompt='Table to query from',
                            help='Table can include hosts, services, contacts etc.')
def qlivestatsdescribe(config, table):
    """ Describe a table in Live Status broker"""

    # Create a Query object
    cfg = configmod.YAMLConfig(config)
    query = Query(cfg.get_broker())

    query = getattr(query, table)

    res = query.Describe()

    click.echo(res)
