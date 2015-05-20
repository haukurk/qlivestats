[![Build Status](https://travis-ci.org/haukurk/qlivestats.svg?branch=master)](https://travis-ci.org/haukurk/qlivestats)
[![Coverage Status](https://coveralls.io/repos/haukurk/qlivestats/badge.svg?branch=master)](https://coveralls.io/r/haukurk/qlivestats?branch=master)
# qlivestats
QLiveStats is a library/client to query the Live Status broker for Nagios.

# Live Status Querying

*qlivestats* support the following tables to get information from:

*qlivestats.hosts* - your Nagios hosts

*qlivestats.services* - your Nagios services, joined with all data from hosts

*qlivestats.hostgroups* - you Nagios hostgroups

*qlivestats.servicegroups* - you Nagios servicegroups

*qlivestats.contactgroups* - you Nagios contact groups

*qlivestats.servicesbygroup* - all services grouped by service groups

*qlivestats.servicesbyhostgroup* - all services grouped by host groups

*qlivestats.hostsbygroup* - all hosts group by host groups

*qlivestats.contacts* - your Nagios contacts

*qlivestats.commands* - your defined Nagios commands

*qlivestats.timeperiods* - time period definitions (currently only name and alias)

*qlivestats.downtimes* - all scheduled host and service downtimes, joined with data from hosts and services.

*qlivestats.comments* - all host and service comments

*qlivestats.log* - a transparent access to the nagios logfiles (include archived ones)ones

*qlivestats.status* - general performance and status information. This table contains exactly one dataset.

*qlivestats.columns* - a complete list of all tables and columns available via Livestatus, including descriptions!

*qlivestats.statehist* - 1.2.1i2 sla statistics for hosts and services, joined with data from hosts, services and log.


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
