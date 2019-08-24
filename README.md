lite-domain-list
================

Lite domain list, based on [v2ray/domain-list-community](https://github.com/v2ray/domain-list-community).


Todo
----

Output:
- [X] Output `dnsmasq` rules
- [ ] And more...

Data parse:
- [X] Remove all comments & empty lines
- [X] Replace `include:`
- [ ] Generate each `domain:`
- [ ] Generate each `keyword:`
- [ ] Generate each `regex:`
- [ ] Generate each `full:`

Usage
-----

```
usage: build.py [-h] [-l] [-s SERVER] [TARGET]

domain-list-community

positional arguments:
  TARGET                target domain-list to build (default: cn)

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            list all buildable domain-lists
  -s SERVER, --server SERVER
                        public dns server (default: 223.5.5.5)
```
