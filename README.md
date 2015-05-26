[![Build Status](https://travis-ci.org/haukurk/qlivestats.svg?branch=master)](https://travis-ci.org/haukurk/qlivestats)
[![Coverage Status](https://coveralls.io/repos/haukurk/qlivestats/badge.svg?branch=master)](https://coveralls.io/r/haukurk/qlivestats?branch=master)
# qlivestats
QLiveStats is a library to query the Live Status broker for Nagios.

# Live Status Querying

Attribute for object *qlivestats.Query*.

| Attribute                        | Description                                                                                 |
|----------------------------------|---------------------------------------------------------------------------------------------|
| *hosts*               | Your Nagios hosts                                                                           |
| *services*            | Your Nagios services joined with all data from hosts                                        |
| *hostgroups*          | You Nagios hostgroups                                                                       |
| *servicegroups*       | You Nagios servicegroups                                                                    |
| *contactgroups*       | You Nagios contact groups                                                                   |
| *servicesbygroup*     | All services grouped by service groups                                                      |
| *servicesbyhostgroup* | All services grouped by host groups                                                         |
| *hostsbygroup*        | All hosts group by host groups                                                              |
| *contacts*            | Your Nagios contacts                                                                        |
| *commands*            | Your defined Nagios commands                                                                |
| *timeperiods*         | Time period definitions (currently only name and alias)                                     |
| *downtimes*           | All scheduled host and service downtimes joined with data from hosts and services.          |
| *comments*            | All host and service comments                                                               |
| *log*                 | A transparent access to the nagios logfiles (include archived ones)ones                     |
| *status*              | General performance and status information. This table contains exactly one dataset.        |
| *columns*             | A complete list of all tables and columns available via Livestatus including descriptions!  |
| *statehist*           | SLA statistics for hosts and services joined with data from hosts services and log. |

Functions for **qlivestas.Query.attribute**, where attributes can be from the above lists:

| Function                        | Description                                                     |
|----------------------------------|-----------------------------------------------------------------|
| *Filter(STRING)*               | Filter your query                                                         | 
| *Column(STRING)*            | Only include certain column (one). Can be chained with more column function calls.|        
| *Columns(STRING)*          | Only Include cartain set of columns (many) seperated with whitespace.                    |
| *Describe()*           | Describe what columns are available for table that have been choosen by using the attributes above. | 

Note that the functions *Filter*, *Column* and *Columns* can be chained:
```
query = Query()
query.hosts.Filter("host_name ~ servername").Filter("acknowledged = 0").Column("host_name").run()
```

# Usage

## Filters

To filter your result set, you use the ```Filter``` function. This allows you to fetch you specific data much faster then by using the whole set.

The following example queries information about ```hosts``` from your LiveStatus broker, that **contains** ```purple``` in the hostname column:

```
import qlivestats

query = qlivestats.Query("/var/spool/livestatus/broker")
result = query.hosts.Filter("host_name ~ purple").run()
```

Following operators are available when using filters:

| symbol  | operation                                   | on numbers  | on texts  |
|-------- |-------------------------------------------- |------------ |---------- |
| `=`       | equality                                    | yes         | yes       |
| `~`       | match regular expression (substring match)  | no          | yes       |
| `=~`      | equality ignoring case                      | no          | yes       |
| `~~`      | regular expression ignoring case            | no          | yes       |
| `<`       | less than                                   | yes         | yes       |
| `>`       | greater than                                | yes         | yes       |
| `<=`      | less or equal                               | yes         | yes       |
| `>=`      | greater or equal                            | yes         | yes       |
| `!=`      | is not equal                                | yes         | yes       |
| `!~`      | does not match regular expression (substring match) | no  | yes       |
| `!=~`     | is not equal when ignoring case             | no          | yes       |
| `!~~`     | does not match regular expression ignoring case | no      | yes       | 

To get more in-depth inforatmion about the LQL (LiveStatus Query Language), please visit https://mathias-kettner.de/checkmk_livestatus.html.

## Columns

You can specifiy what columns to include when querying information:

The following example only selects ```perf_data``` when displaying information from you **services**:

```
import qlivestats

query = qlivestats.Query("/var/spool/livestatus/broker")
result = query.services.Column('perf_data').Filter("description = CPU utilization")                                                             
```

Note that we have a chained function ```Filter``` that filters information that has **description** equal to ```CPU utilization```.
