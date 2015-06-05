#!/usr/bin/env python

import os, shutil, subprocess, sys, tempfile

def main(argv):
    
    if len(argv[1:]) != 2:
        print >> sys.stderr, 'Run cdec mbr (or any k-best processing command) on multiple cores'
        print >> sys.stderr, 'cdec mbr executable is cdec/mteval/mbr_kbest'
        print >> sys.stderr, 'Usage: {0} mbr-cmd jobs < in.kbest > out.mbr'.format(argv[0])
        sys.exit(1)
    
    cmd = argv[1]
    jobs = int(argv[2])
    files = []
    procs = []
    out = []
    
    # Work dir
    tmp = tempfile.mkdtemp(prefix='mbr.', dir=os.path.abspath(os.curdir))
    
    # Split k-best
    print >> sys.stderr, 'Splitting k-best {0} ways...'.format(jobs)
    for i in range(jobs):
        files.append(open(os.path.join(tmp, '{0}.nbest'.format(i)), 'w'))
    i = -1
    idx = '-1'
    for line in sys.stdin:
        f = line.split(' ||| ')
        if f[0] != idx:
            i = (i + 1) % jobs
            idx = f[0]
        print >> files[i], line.rstrip('\n')
    for i in range(jobs):
        files[i].close()
    
    # Run mbr
    print >> sys.stderr, 'Running {0} instances of {1}...'.format(jobs, cmd)
    for i in range(jobs):
        out.append(open(os.path.join(tmp, '{0}.mbr'.format(i)), 'w'))
        procs.append(subprocess.Popen([cmd], stdin=open(os.path.join(tmp, '{0}.nbest'.format(i))), stdout=out[i]))
    for i in range(jobs):
        procs[i].wait()
        out[i].close()
    
    # Combine output
    out = []
    for i in range(jobs):
        out.append(open(os.path.join(tmp, '{0}.mbr'.format(i))))
    i = 0
    while out:
        line = out[i].readline()
        if line:
            print line.rstrip('\n')
        else:
            out.pop(i)
        if len(out) == 0:
            break
        i = (i + 1) % len(out)

    # Cleanup
    print >> sys.stderr, 'Cleanup...'
    shutil.rmtree(tmp)

if __name__ == '__main__' : main(sys.argv)
