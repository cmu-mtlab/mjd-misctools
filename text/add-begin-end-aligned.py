#!/usr/bin/env python

import itertools, os, sys

def main(argv):

    if len(argv[1:]) != 6:
        print >> sys.stderr, 'Usage: {0} corpus.fr corpus.en corpus.align corpus.fr.be corpus.en.be corpus.align.be'.format(argv[0])
        print >> sys.stderr, 'Add begin <s> and end </s> sentence markers to corpus and adjust alignments'

        sys.exit(2)

    (in_f, in_e, in_a) = (open(f, 'r') for f in argv[1:4])
    (out_f, out_e, out_a) = (open(f, 'w') for f in argv[4:7])

    for (f, e, a) in itertools.izip(in_f, in_e, in_a):
        print >> out_f, '<s> {0} </s>'.format(f.strip())
        print >> out_e, '<s> {0} </s>'.format(e.strip())
        aplus = ' '.join(('-'.join(str(int(y) + 1) for y in x.split('-')) for x in a.split()))
        print >> out_a, '0-0 {0} {1}-{2}'.format(aplus, len(f.split()) + 1, len(e.split()) + 1,)

    for f in (out_f, out_e, out_a):
        f.close()

if __name__ == '__main__':
    main(sys.argv)
