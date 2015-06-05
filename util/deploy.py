#!/usr/bin/env python

import sys
import subprocess
import os

job = '''#!/bin/bash
# the queue to be used.
#PBS -q shared
# specify your project allocation
#PBS -A cmu126
# number of nodes and number of processors per node requested
#PBS -l nodes=1:ppn=4
# requested Wall-clock time.
#PBS -l walltime=2:00:00
# name of the standard out file to be "output-file".
#PBS -o {log}/{i}.out
#PBS -e {log}/{i}.err
# name of the job
#PBS -N deploy.{i}
#PBS -V
'''

if len(sys.argv[1:]) != 1:
    print 'Usage: {} scratch'.format(sys.argv[0])
    sys.exit(2)

scratch = os.path.abspath(sys.argv[1])
if not os.path.exists(scratch):
    os.mkdir(scratch)

i = 0
for line in sys.stdin:
    script = os.path.join(scratch, str(i)) + '.sh'
    s_out = open(script, 'w')
    print >> s_out, job.format(log=scratch, i=i)
    print >> s_out, 'cd {}'.format(os.path.abspath(os.curdir))
    print >> s_out, line.strip()
    s_out.close()
    subprocess.call(['qsub', script])
    i += 1
