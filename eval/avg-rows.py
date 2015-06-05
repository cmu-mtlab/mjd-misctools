#!/usr/bin/env python
 
import sys
for line in sys.stdin:
    f = [float(x) for x in line.split()]
    print sum(f) / len(f)
