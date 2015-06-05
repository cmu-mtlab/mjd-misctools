#!/usr/bin/env python

import math, sys

def main(argv):

    print >> sys.stderr, 'Usage: {0} < in.ngrams > out.arpa'.format(argv[0])
    print >> sys.stderr, 'Lines are SRI format: `word1 word2 etc.\\tscore\', space delim words, tab delim score'

    ngrams = [{'<s>': -2.0, '</s>': -2.0, '<unk>': -2.0}]

    for line in sys.stdin:
        (ngram, score) = line.split('\t')
        score = math.log10(float(score) / 100)
        n = ngram.count(' ') + 1
        while len(ngrams) < n:
            ngrams.append({})
        ngrams[n-1][ngram] = score

    print ''
    print '\\data\\'
    for i in range(len(ngrams)):
        print 'ngram {0}={1}'.format(i+1, len(ngrams[i]))
    for i in range(len(ngrams) - 1):
        print ''
        print '\\{0}-grams:'.format(i+1)
        for ngram in sorted(ngrams[i]):
            print '{0}\t{1}\t0'.format(ngrams[i][ngram], ngram)
    i = len(ngrams) - 1
    print ''
    print '\\{0}-grams:'.format(i+1)
    for ngram in sorted(ngrams[i]):
        print '{0}\t{1}'.format(ngrams[i][ngram], ngram)
    print ''
    print '\\end\\'

if __name__ == '__main__' : main(sys.argv)
