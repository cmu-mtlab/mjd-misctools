#!/usr/bin/env python

import sys

def main(argv):

    print >> sys.stderr, '{0} [metric] < in.kbest > out.oracle'.format(argv[0])

    metric = argv[1] if len(argv[1:]) > 0 else 'bleu'
    mrank = metric + 'Rank=0'

    for line in sys.stdin:
        f = line.split('|||')
        if f[-2].find(mrank) != -1:
            print f[1].strip()

if __name__ == '__main__' : main(sys.argv)
