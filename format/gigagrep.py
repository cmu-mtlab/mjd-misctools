#!/usr/bin/env python

import sys

def main():

    for line in sys.stdin:
        line = line.strip()
        if line[0] == '<' and line[-1] == '>':
            pass
        else:
            print line

if __name__ == '__main__':
    main()
