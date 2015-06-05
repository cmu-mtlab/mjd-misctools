#!/usr/bin/env python

import sys

def main(argv):
    
    if len(argv[1:]) != 1:
        print >> sys.stderr, 'Usage: {0} retained < in > out'.format(argv[0])
        sys.exit(2)

    lc = 0
    for idx in open(argv[1]):
        i = int(idx)
        line = ''
        while lc < i:
            lc += 1
            line = sys.stdin.readline()
        sys.stdout.write(line)

if __name__ == '__main__':
    main(sys.argv)
