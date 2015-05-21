[![Build Status](https://travis-ci.org/haukurk/qlivestats.svg?branch=master)](https://travis-ci.org/haukurk/qlivestats)
[![Coverage Status](https://coveralls.io/repos/haukurk/qlivestats/badge.svg?branch=master)](https://coveralls.io/r/haukurk/qlivestats?branch=master)
# qlivestats
QLiveStats is a library/client to query the Live Status broker for Nagios.

# Live Status Querying

| Attribute                        | Description                                                                                 |
|----------------------------------|---------------------------------------------------------------------------------------------|
| *qlivestats.hosts*               | Your Nagios hosts                                                                           |
| *qlivestats.services*            | Your Nagios services joined with all data from hosts                                        |
| *qlivestats.hostgroups*          | You Nagios hostgroups                                                                       |
| *qlivestats.servicegroups*       | You Nagios servicegroups                                                                    |
| *qlivestats.contactgroups*       | You Nagios contact groups                                                                   |
| *qlivestats.servicesbygroup*     | All services grouped by service groups                                                      |
| *qlivestats.servicesbyhostgroup* | All services grouped by host groups                                                         |
| *qlivestats.hostsbygroup*        | All hosts group by host groups                                                              |
| *qlivestats.contacts*            | Your Nagios contacts                                                                        |
| *qlivestats.commands*            | Your defined Nagios commands                                                                |
| *qlivestats.timeperiods*         | Time period definitions (currently only name and alias)                                     |
| *qlivestats.downtimes*           | All scheduled host and service downtimes joined with data from hosts and services.          |
| *qlivestats.comments*            | All host and service comments                                                               |
| *qlivestats.log*                 | A transparent access to the nagios logfiles (include archived ones)ones                     |
| *qlivestats.status*              | General performance and status information. This table contains exactly one dataset.        |
| *qlivestats.columns*             | A complete list of all tables and columns available via Livestatus including descriptions!  |
| *qlivestats.statehist*           | SLA statistics for hosts and services joined with data from hosts services and log. |

# Filters

Its easy to use filters:


```
import qlivestats

query = qlivestats.Query("/var/spool/livestatus/broker")

result = query.hosts.filter("hostname ~ purple").run()
```

operators available for filters:

| symbol  | operation                                   | on numbers  | on texts  |
|-------- |-------------------------------------------- |------------ |---------- |
| =       | equality                                    | yes         | yes       |
| ~       | match regular expression (substring match)  | no          | yes       |
| =~      | equality ignoring case                      | no          | yes       |
| ~~      | regular expression ignoring case            | no          | yes       |
| <       | less than                                   | yes         | yes       |
| >       | greater than                                | yes         | yes       |
| <=      | less or equal                               | yes         | yes       |
| >=      | greater or equal                            | yes         | yes       |
| !=      | is not equal                                | yes         | yes       |
| !~      | does not match regular expression (substring match) | no  | yes       |
| !=~     | is not equal when ignoring case             | no          | yes       |
| !~~     | does not match regular expression ignoring case | no      | yes       | 

To get more in-depth inforatmion about the LQL (LiveStatus Query Language), please visit https://mathias-kettner.de/checkmk_livestatus.html.

# Columns

Its easy to include only columns that you are interested in:

```
import qlivestats

query = qlivestats.Query("/var/spool/livestatus/broker")

result = query.services.Column('perf_data').Filter("description ~ CPU util")                                                             
```
