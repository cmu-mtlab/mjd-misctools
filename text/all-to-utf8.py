#!/usr/bin/env python

import sys
from BeautifulSoup import UnicodeDammit

def main(argv):

    print >> sys.stderr, 'Mystery text goes in, UTF-8 comes out.  No-op on UTF-8 input.'
    print >> sys.stderr, '-w to detect/convert at the word level (assumes space sanity)'
    print >> sys.stderr, '-d to drop lines that are suspected invalid encodings (last-resort to'
    print >> sys.stderr, '   windows-1252 and contain no spaces.  Check stderr to see what drops.)'

    wlevel = True if '-w' in argv[1:] else False
    drop = True if '-d' in argv[1:] else False

    lc = 0
    for line in sys.stdin:
        line = line.rstrip('\n')
        lc += 1
        # If not valid utf-8
        try:
            unicode(line, 'utf-8')
        # Try to detect encoding
        except:
            # By word
            if wlevel:
                line = ' '.join([UnicodeDammit(w).unicode.encode('utf-8') for w in line.split()])
            # Full line
            else:
                u = UnicodeDammit(line)
                line = u.unicode.encode('utf-8')
                # Reasonable guess: last-resort encoding and no spaces
                if drop and u.originalEncoding == 'windows-1252' and ' ' not in line:
                    print >> sys.stderr, 'Dropping line {0}: {1}'.format(lc, line)
                    line = ''
        print line

if __name__ == '__main__' : main(sys.argv)

