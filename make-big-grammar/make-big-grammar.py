#!/usr/bin/env python

import getopt, os, subprocess, sys, time

# Smaller batch = more extract jobs
BATCH_SIZE = '100'

COPY = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'copy-grammars.py')
WAIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wait-done.py')

# This script written for trestles, change as needed
JOB_SCRIPT = '''#!/bin/bash
# Written for trestles
#PBS -q shared
#PBS -l nodes=1:ppn=4
#PBS -l walltime=24:00:00
#PBS -o {work}/logs/{f}.out
#PBS -e {work}/logs/{f}.err
#PBS -N bg.{f}
#PBS -V

echo "Start: $(date)"

# Write to scratch to avoid lustre errors
cd /scratch/$USER/$PBS_JOBID/

# Start moving finished grammars in background
mkdir -p {work}/{f}.grammar
{copy} `pwd` {work}/{f}.grammar &

# Extract
time cat {work}/{f} | python -m cdec.sa.extract -c {ini} -g `pwd`

# Tell copy script to exit and wait
touch END
{wait} `pwd`

echo "End: $(date)"
'''

def main(argv):
   
    # defaults
    batch_size = BATCH_SIZE

    opts, args = getopt.getopt(argv[1:], 'fb:m:')
    for o, a in opts:
        if o == '-b':
            batch_size = a

    if len(args) != 3:
        print >> sys.stderr, 'Use sa-extract to create large grammar in batches'
        print >> sys.stderr, 'Usage: {0} [options] extract.ini in.txt workdir'.format(argv[0])
        print >> sys.stderr, '  -b N  batch size, default=100'
        sys.exit(1)

    ext_ini = os.path.abspath(args[0])
    in_file = os.path.abspath(args[1])
    work_dir = os.path.abspath(args[2])

    if os.path.exists(work_dir):
        print >> sys.stderr, 'Exiting - workdir {0} exists'.format(work_dir)
        sys.exit(1)
    
    os.mkdir(work_dir)
    
    subprocess.call('split -l{size} -da7 {0} {1}/'.format(in_file, work_dir, size=batch_size).split())
    
    splits = os.listdir(work_dir)
    
    script_dir = os.path.join(work_dir, 'scripts')
    log_dir = os.path.join(work_dir, 'logs')
    os.mkdir(script_dir)
    os.mkdir(log_dir)
    
    for f in splits:
        script = os.path.join(script_dir, '{0}.sh'.format(f))
        script_out = open(script, 'w')
        print >> script_out, JOB_SCRIPT.format(work=work_dir, f=f, ini=ext_ini, copy=COPY, wait=WAIT)
        script_out.close()
        print >> sys.stderr, f
        subprocess.call(['qsub', script])

if __name__ == '__main__' : main(sys.argv)
