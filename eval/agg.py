#!/usr/bin/env python

import sys
f = float if len(sys.argv) > 1 and sys.argv[1] == '-f' else int
total = 0
for line in sys.stdin:
    total += f(line.strip())
print total
