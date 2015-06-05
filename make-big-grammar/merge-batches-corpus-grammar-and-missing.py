#!/usr/bin/env python

import os, shutil, sys

START = 0

def FMT(i):
    return '{0:07d}'.format(i)

def main(argv):

    if len(argv[1:]) != 2:
        print >> sys.stderr, 'Merge batches from make-big-grammr into corpus and grammar plus file for lines with missing grammars'
        print >> sys.stderr, ''
        print >> sys.stderr, 'Usage: {0} mbg-dir out-dir'.format(argv[0])
        sys.exit(2)

    mbg_dir = argv[1]
    out_dir = argv[2]

    if os.path.exists(out_dir):
        print >> sys.stderr, '{0} exists, exiting'.format(out_dir)
        sys.exit(1)

    wc = 0
    for line in open(os.path.join(mbg_dir, FMT(START))):
        wc += 1

    out_gram_dir = os.path.join(out_dir, 'grammar')

    os.mkdir(out_dir)
    os.mkdir(out_gram_dir)
    out_cor = open(os.path.join(out_dir, 'corpus'), 'w')
    out_miss = open(os.path.join(out_dir, 'missing'), 'w')

    batch = START
    txt = os.path.join(mbg_dir, FMT(batch))
    i = 0
    done = False

    while not done:
        in_gram_dir = txt + '.grammar'
        gi = 0
        good = 0
        miss = 0
        for line in open(txt):
            gram = os.path.join(in_gram_dir, 'grammar.{0}.gz'.format(gi))
            if os.path.exists(gram):
                out_cor.write(line)
                shutil.copy(gram, os.path.join(out_gram_dir, 'grammar.{0}.gz'.format(i)))
                i += 1
                good += 1
            else:
                out_miss.write(line)
                # no grammar
                miss += 1
            gi += 1
        print >> sys.stderr, '{0}: {1} good, {2} missing'.format(txt, good, miss)
        batch += 1
        txt = os.path.join(mbg_dir, FMT(batch))
        if not os.path.exists(txt):
            done = True

    out_cor.close()
    out_miss.close()

if __name__ == '__main__':
    main(sys.argv)
