#!/usr/bin/env python

# Pipe XML source file to this script

from sys import stdin
import re

GENRES = { 'nw': 'news',
           'wb': 'web',
  }

genre = ''
for line in stdin:
    r = re.search('^\s*<doc .*genre="([^"]+)".*', line, re.I)
    if r:
        genre = GENRES[r.group(1)]
        continue
    r = re.search('^\s*<seg', line, re.I)
    if r:
        print genre
