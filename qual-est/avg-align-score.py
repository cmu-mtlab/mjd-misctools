#!/usr/bin/env python

import numpy
from sys import argv, stdin
from math import log, exp

x = []
y = []

eval = True if len(argv) == 2 and argv[1] == 'eval' else False

while True:
    line = stdin.readline()
    if not line:
        break
    score = float(line.split(':')[1].strip())
    stdin.readline() # tgt
    align = stdin.readline()
    links = 0
    words = 0
    unaligned = 0
    j = -3 # Start at beginning of line
    null = True # start with null word
    while True:
        i = align.find('({', j + 3)
        if i == -1:
            break
        j = align.find('})', i + 3)
        l = len(align[i+3:j-1].split())
        links += l
        # Do not count null word
        if null:
            null = False
            continue
        if l == 0:
            unaligned += 1
        words += 1
    s = log(score) / links
    a = float(words - unaligned) / words
    if eval:
        print s, a
    else:
        x.append(s)
        y.append(a)
if not eval:
    print 'Avg alignment score:'
    print numpy.mean(x), numpy.std(x)
    print 'Avg aligned link ratio:'
    print numpy.mean(y), numpy.std(y)
