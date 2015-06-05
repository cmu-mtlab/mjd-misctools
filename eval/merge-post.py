#!/usr/bin/env python

import itertools, sys

def main(argv):
    
    if len(argv[1:]) < 2 or len(argv[1:]) % 2 != 0:
        print >> sys.stderr, 'Merge post-edits for lowest HTER (closest reference for each segment)'
        print >> sys.stderr, 'Usage: {0} post1 hter1 [post2 hter2 ...]'.format(argv[0])
        sys.exit(1)
    
    for hter in itertools.izip(*[open(x) for x in argv[1:]]):
        best = ['', 9999]
        for i in range(0, len(hter), 2):
            if float(hter[i+1]) < best[1]:
                best = [hter[i], float(hter[i+1])]
        print best[0].strip()
        
if __name__ == '__main__' : main(sys.argv)
