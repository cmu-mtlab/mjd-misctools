#!/usr/bin/env python

import os, sys, time

DONE = 'DONE'

def main(argv):

    if len(argv[1:]) != 1:
        print >> sys.stderr, 'Wait for {0} to exist in dir'.format(DONE)
        print >> sys.stderr, 'Usage: {0} dir'.format(argv[0])
        sys.exit(1)

    src = argv[1]

    while True:
        files = os.listdir(src)
        if DONE in files:
            break
        time.sleep(10)

if __name__ == '__main__' : main(sys.argv)
