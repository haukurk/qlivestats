[![Build Status](https://travis-ci.org/haukurk/qlivestats.svg?branch=master)](https://travis-ci.org/haukurk/qlivestats)
[![Coverage Status](https://coveralls.io/repos/haukurk/qlivestats/badge.svg?branch=master)](https://coveralls.io/r/haukurk/qlivestats?branch=master)
# qlivestats
QLiveStats is a library/client to query the Live Status broker for Nagios.

# Filters

Its easy to use filters:


```
import qlivestats

query = qlivestats.Query("/var/spool/livestatus/broker")

result = query.hosts.filter("hostname ~ purple").run()

print result

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
