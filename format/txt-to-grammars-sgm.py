#!/usr/bin/env python

import os, sys

def main(argv):

    if len(argv[1:]) != 1:
        print >> sys.stderr, 'Usage: {0} grammar-dir < in.txt > out.sgm'.format(argv[0])
        sys.exit(2)

    gdir = argv[1]

    for (line, f) in zip(sys.stdin, sorted(os.listdir(gdir), cmp=lambda x, y: cmp(int(x.split('.')[-2]), int(y.split('.')[-2])))):
        print '<seg grammar="{0}" id="{1}">{2}</seg>'.format(os.path.join(gdir, f), f.split('.')[-2], line.strip())

if __name__ == '__main__':
    main(sys.argv)
