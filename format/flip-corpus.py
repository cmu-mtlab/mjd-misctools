#!/usr/bin/env python

import sys

def main():
    
    for line in sys.stdin:
        print '{1} ||| {0}'.format(*(f.strip() for f in line.split('|||')))

if __name__ == '__main__':
    main()
