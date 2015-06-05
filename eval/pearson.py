#!/usr/bin/env python

from scipy import stats
from sys import stdin

x, y = [], []

for line in stdin:
    f = line.split()
    x.append(float(f[0]))
    y.append(float(f[1]))

print stats.pearsonr(x, y)
