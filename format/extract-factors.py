#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

delims = u'|·'

def main(argv):

    if len(argv[1:]) != 2:
        print >> sys.stderr, 'Usage: {0} N D < in > out'.format(argv[0])
        print >> sys.stderr, 'Extract factor N from each token using delimiter D'
        print >> sys.stderr, ''
        print >> sys.stderr, 'N is 1-indexed'
        print >> sys.stderr, ''
        print >> sys.stderr, 'Pick delimiter:'
        print >> sys.stderr, delims
        print >> sys.stderr, ''.join((str(i) for i in range(1, len(delims) + 1)))
        sys.exit(2)

    N = int(argv[1]) - 1
    delim = delims[int(argv[2]) - 1].encode('UTF-8')

    for line in sys.stdin:
        print ' '.join((word.split(delim)[N] for word in line.split()))

if __name__ == '__main__':
    main(sys.argv)
