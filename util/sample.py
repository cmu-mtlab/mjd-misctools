#!/usr/bin/env python

import collections, sys, subprocess, threading

def main(argv):

    if len(argv[1:]) != 1:
        print >> sys.stderr, 'Usage: {0} N < in > out'.format(sys.argv[0])
        print >> sys.stderr, 'Sample every Nth line'
        sys.exit(1)

    # Queue up jobs and N end markers
    N = int(argv[1])
    i = 0
    for line in sys.stdin:
        i += 1
        if i % N == 0:
            sys.stdout.write(line)

if __name__ == '__main__' : main(sys.argv)
