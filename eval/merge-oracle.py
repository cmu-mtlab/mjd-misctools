#!/usr/bin/env python

import itertools, sys

def main(argv):
    
    if len(argv[1:]) < 2 or len(argv[1:]) % 2 != 0:
        print >> sys.stderr, 'Merge translations for highest score (oracle)'
        print >> sys.stderr, 'Usage: {0} hyp1 score1 [hyp2 score2 ...]'.format(argv[0])
        sys.exit(1)
    
    for hter in itertools.izip(*[open(x) for x in argv[1:]]):
        best = ['', float('-inf')]
        for i in range(0, len(hter), 2):
            if float(hter[i+1]) > best[1]:
                best = [hter[i], float(hter[i+1])]
        print best[0].strip()
        
if __name__ == '__main__' : main(sys.argv)
