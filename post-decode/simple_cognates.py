#!/usr/bin/env python

import sys, unicodedata

def main(argv):

    if len(argv[1:]) != 2:
        print >> sys.stderr, 'Words seen less than `minocc\' times in frequency list processed as cognates'
        print >> sys.stderr, 'Usage, {0} freq minocc < in.tok > out.tok'.format(argv[0])
        sys.exit(1)

    d = set()
    minocc = int(argv[2])
    for line in open(argv[1]):
        (occ, word) = line.split()
        if int(occ) >= minocc:
            d.add(word)

    for line in sys.stdin:
        words = line.split()
        for i in range(len(words)):
            # Don't touch proper nouns
            if words[i][0].islower() and words[i] not in d:
                try:
                    unicode(words[i], 'ascii')
                except:
                    print >> sys.stderr, words[i],
                    words[i] = ''.join([c for c in unicodedata.normalize('NFD', unicode(words[i], 'utf-8')) if unicodedata.category(c) != 'Mn']).encode('utf-8')
                    print >> sys.stderr, '->', words[i]
        print ' '.join(words)

if __name__ == '__main__' : main(sys.argv)
