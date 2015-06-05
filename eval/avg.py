#!/usr/bin/env python

import sys
f = []
for line in sys.stdin:
    f.append(float(line.strip()))
print sum(f) / (len(f) if len(sys.argv) == 1 else float(sys.argv[1]))
