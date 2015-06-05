#!/usr/bin/env python

import numpy
from sys import argv

text = open(argv[1])
scores = open(argv[2])

x = []
eval = True if len(argv) == 4 and argv[3] == 'eval' else False 
for line in text:
    wc = len(line.split()) + 1 # </s>
    s = float(scores.readline().strip())
    avg = s / wc
    if eval:
        print avg
    else:
        x.append(avg)
if not eval:
    mean = numpy.mean(x)
    std = numpy.std(x)
    print mean, std
