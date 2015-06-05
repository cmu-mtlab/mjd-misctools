#!/usr/bin/env python

import os, subprocess, sys, time

END = 'END'
DONE = 'DONE'

def main(argv):

    if len(argv[1:]) != 2:
        print >> sys.stderr, 'Gzip and copy grammars ending in .0, .1, etc. from src to tgt'
        print >> sys.stderr, 'Run in background to copy files from scratch dir to final dir'
        print >> sys.stderr, 'Exits when file {0} is last file in srcdir'.format(END)
        print >> sys.stderr, 'Creates file {0}, run wait-done.py to wait for exit'.format(DONE)
        print >> sys.stderr, 'Usage: {0} srcdir tgtdir'.format(argv[0])
        sys.exit(1)

    src = argv[1]
    tgt = argv[2]

    while True:
        files = os.listdir(src)
        # done
        if len(files) == 1 and files[0] == END:
            break
        # wait for more files (at least one finished and one current)
        elif len(files) < 2:
            time.sleep(30)
            continue
        files.sort(cmp=lambda x,y:
          1 if x == END \
          else -1 if y == END \
          else cmp(int(x.split('.')[-1]), int(y.split('.')[-1])))
        # print files[0]
        subprocess.call(['gzip', os.path.join(src, files[0])])
        subprocess.call(['mv', files[0] + '.gz', tgt])

    subprocess.call(['touch', DONE])

if __name__ == '__main__' : main(sys.argv)
