#!/usr/bin/env python

import itertools, sys

if len(sys.argv[1:]) != 1:
    print >> sys.stderr, 'Usage: {0} N'.format(sys.argv[0])
    sys.exit(2)
n = int(sys.argv[1]) - 1
for line in sys.stdin:
    print line.split('|||')[n].strip()
