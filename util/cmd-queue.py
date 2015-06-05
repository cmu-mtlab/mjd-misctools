#!/usr/bin/env python

import collections, sys, subprocess, threading

def main(argv):

    if len(argv[1:]) != 1:
        print >> sys.stderr, 'Usage: cat cmd-list | {0} N'.format(sys.argv[0])
        print >> sys.stderr, 'Reads one command per line from stdin'
        print >> sys.stderr, 'Keeps N jobs running, output order _not_ guaranteed'
        print >> sys.stderr, 'Runs commands through shell (shell=True)'
        sys.exit(1)

    # Queue up jobs and N end markers
    N = int(argv[1])
    queue = collections.deque([])
    for line in sys.stdin:
        queue.append(line.strip())
    for i in range(N):
        queue.append(-1)

    # Run N workers
    threads = []
    for i in range(N):
        t = threading.Thread(target=run, args=(queue,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

# Run commands until end of queue
def run(queue):
    while True:
        cmd = queue.popleft()
        if cmd == -1:
            return
        subprocess.call(cmd, shell=True)

if __name__ == '__main__' : main(sys.argv)
