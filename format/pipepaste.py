#!/usr/bin/env python

import itertools, sys

for lines in itertools.izip_longest(*(open(f) for f in sys.argv[1:])):
    print ' ||| '.join(line.strip() for line in lines)
