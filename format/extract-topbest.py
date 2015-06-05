#!/usr/bin/env python

from sys import stdin

i = '-1'
for line in stdin:
    f = line.split('|||')
    if f[0].strip() != i:
        print f[1].strip()
        i = f[0].strip()
