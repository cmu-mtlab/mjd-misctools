#!/usr/bin/env python

import codecs, sys

sys.stdin = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def unk(word):

    if len(word) <= 3:
        return '<unk_1_3>'
    if len(word) <= 7:
        return '<unk_4_7>'
    else:
        return '<unk_8_n>'

def main(argv):

    if len(argv[1:]) != 1:
        print >> sys.stderr, 'Usage: {0} vocab < in > out'.format(argv[0])
        sys.exit(2)

    vocab = set(word.strip() for word in codecs.open(argv[1], 'rb', 'utf-8'))

    for line in sys.stdin:
        print ' '.join(word if word in vocab else unk(word) for word in line.split())

if __name__ == '__main__':
    main(sys.argv)
