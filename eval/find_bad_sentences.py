#!/usr/bin/env python

import itertools
import sys

def main(argv):

    if len(argv[1:]) != 4:
        sys.stderr.write('usage: {} src tgt mt bleu\n'.format(argv[0]))
        sys.exit(2)

    data = list(itertools.izip((float(f.strip()) for f in open(argv[4])), open(argv[1]), open(argv[2]), open(argv[3])))

    for (b, s, t, m) in sorted(data):
        sys.stdout.write('{:0.4f} ||| {} ||| {} ||| {}\n'.format(b, s.strip(), t.strip(), m.strip()))

if __name__ == '__main__':
    main(sys.argv)
