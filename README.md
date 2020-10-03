nautilus-desktop
================

A nautilus extension to quickly create a Shell application starter.
Well actually it creates a _.desktop_ file within _.local/share/applications/_ with a hash of the application name to avoid collisions.

Installation
------------

You need _python_ and _nautilus-python_ on your system, then run:
```bash
sudo python setup.py install
```
This will install the extension to _/usr/share/nautilus-python/extensions_.


Note
------------
This forked version works on Python2, since the original version was not working on my system (Ubuntu 20.04)
