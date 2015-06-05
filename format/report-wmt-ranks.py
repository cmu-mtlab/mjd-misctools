#!/usr/bin/env python

import csv, os, sys

lang = {'en': 'English', 'cz': 'Czech', 'de': 'German', 'fr': 'French'}

def main(argv):
    
    if len(argv[1:]) < 4:
        print >> sys.stderr, 'Create a (very basic) report of ranked WMT system outputs'
        print >> sys.stderr, 'Usage: {0} lang-pair in.csv ref sys1.out [sys2.out ...]'.format(argv[0])
        sys.exit(1)
    
    (src, tgt) = [lang[x] for x in argv[1].split('-')]

    csv_in = csv.reader(open(argv[2]))
    
    seg = {} # seg[sys][id] = text
    
    ref_lines = [line.strip() for line in open(argv[3])]
    seg['_ref'] = dict([(i + 1, ref_lines[i]) for i in range(len(ref_lines))])
    for f in argv[4:]:
        s = os.path.basename(f).split('.')[2] # testset.lang-pair.sys
        f_lines = [line.strip() for line in open(f)]
        seg[s] = dict([(i + 1, f_lines[i]) for i in range(len(f_lines))])
    tok = csv_in.next()
    col = dict(zip(tok, range(len(tok))))
    # One row contains one n-way rank judgment
    for row in csv_in:
        if row[col['srclang']] == src and row[col['trglang']] == tgt:
            # Collect rank data
            idx = int(row[col['srcIndex']])
            report = dict([(i, []) for i in range(1, 6)])
            for i in range(1, 6):
                rank = int(row[col['system{0}rank'.format(i)]])
                if rank != -1:
                    report[rank].append(seg[row[col['system{0}Id'.format(i)]]][idx])
            # Print rank report
            print idx
            print 'ref: {0}'.format(seg['_ref'][idx])
            print ''
            for i in range(1, 6):
                for text in report[i]:
                    print '{0}:   {1}'.format(i, text)
                if report[i]:
                    print ''

if __name__ == '__main__' : main(sys.argv)