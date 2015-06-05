#!/usr/bin/env python

import sys

def main():
    
    for line in sys.stdin:
        print ' '.join('{0}-{1}'.format(j, i) for (j, i) in sorted((int(j), int(i)) for (i, j) in (link.split('-') for link in line.split())))

if __name__ == '__main__':
    main()
