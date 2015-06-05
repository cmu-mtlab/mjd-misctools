#!/usr/bin/env python

import os, shutil, sys

START = 0

def FMT(i):
    return '{0:07d}'.format(i)

def main(argv):

    if len(argv[1:]) < 2:
        print >> sys.stderr, 'Merge merged batches'
        print >> sys.stderr, ''
        print >> sys.stderr, 'Usage: {0} out-dir merged-dir1 [merged-dir2 ...]'.format(argv[0])
        sys.exit(2)

    out_dir = argv[1]
    dirs = argv[2:]

    if os.path.exists(out_dir):
        print >> sys.stderr, '{0} exists, exiting'.format(out_dir)
        sys.exit(1)

    everything = [] # (text, grammar-file)

    for d in dirs:
        print >> sys.stderr, d
        corpus = open(os.path.join(d, 'corpus'))
        i = 0
        for line in corpus:
            gram = os.path.join(d, 'grammar', 'grammar.{0}.gz'.format(i))
            everything.append((line, gram))
            i += 1

    # When in doubt, sort it out
    everything.sort(cmp=lambda x,y: cmp(x[0], y[0]))

    os.mkdir(out_dir)
    corpus_out = open(os.path.join(out_dir, 'corpus'), 'w')
    gram_dir = os.path.join(out_dir, 'grammar')
    os.mkdir(gram_dir)

    i = 0
    for (line, gram) in everything:
        corpus_out.write(line)
        shutil.copy(gram, os.path.join(gram_dir, 'grammar.{0}.gz'.format(i)))
        i += 1
    corpus_out.close()

if __name__ == '__main__':
    main(sys.argv)
