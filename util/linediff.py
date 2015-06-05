#!/usr/bin/env python

import itertools, sys

def main(argv):
    
    if len(argv[1:]) != 2:
        print >> sys.stderr, 'Usage: {0} file1 file2'.format(argv[0])
        sys.exit(2)

    lc = 0
    for (i, j) in itertools.izip_longest(open(argv[1]), open(argv[2])):
        lc += 1
        if i != j:
            print lc
            sys.stdout.write(i)
            sys.stdout.write(j)

if __name__ == '__main__':
    main(sys.argv)
