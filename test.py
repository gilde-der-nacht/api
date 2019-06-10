#!/usr/bin/env python3

# https://docs.python.org/3/library/urllib.request.html#module-urllib.request

import urllib.request

print(urllib.request.urlopen('http://rollenspieltage.ch/').read())
