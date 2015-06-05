#!/usr/bin/env python

import csv, sys

def main(argv):

    if len(argv[1:]) < 1:
        print >> sys.stderr, 'Usage: {0} <csv-file> [col-id]'.format(argv[0])
        print >> sys.stderr, 'Prints column ids, extracts col-id if provided'
        sys.exit(1)

    reader = csv.reader(open(sys.argv[1]))
    i = int(sys.argv[2]) if len(argv[1:]) > 1 else -1

    header = reader.next()
    print >> sys.stderr, ', '.join(['{0}: {1}'.format(x[1], x[0]) for x in zip(range(len(header)), header)])

    if i == -1:
        sys.exit(0)

    for line in reader:
        if '\n' in line[i]:
            print >> sys.stderr, line[i]
        print line[i].replace('\n', ' ')

if __name__ == '__main__' : main(sys.argv)
