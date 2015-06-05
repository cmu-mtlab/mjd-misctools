#!/usr/bin/env python

import collections
import operator
import subprocess
import sys

def main():

    p = subprocess.Popen(['qstat', '-f'], stdout=subprocess.PIPE)

    running = collections.defaultdict(int)
    queued = collections.defaultdict(int)

    user = ''
    state = ''
    nodes = 0
    ppn = 0

    for line in p.stdout:
        if ' = ' not in line:
            continue
        (k, v) = line.strip().split(' = ')
        if k == 'Job_Owner':
            user = v.split('@')[0]
        elif k == 'job_state':
            state = v
        elif k == 'Resource_List.nodes':
            (nodes, ppn) = (int(i.split(':')[0]) for i in v.split(':ppn='))
            if state == 'R':
                running[user] += (nodes * ppn)
            elif state == 'Q':
                queued[user] += (nodes * ppn)

    for u in queued:
        running[u]

    sys.stdout.write('CPU usage:\n')
    sys.stdout.write('----------------------\n')
    sys.stdout.write('user           R     Q\n')
    sys.stdout.write('----------------------\n')
    for (u, c) in sorted(running.iteritems(), key=operator.itemgetter(1), reverse=True):
        sys.stdout.write('{:10} {:5} {:5}\n'.format(u, c, queued[u]))

if __name__ == '__main__':
    main()
