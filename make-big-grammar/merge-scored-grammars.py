#!/usr/bin/env python

import gzip, os, sys

def main(argv):

    if len(argv[1:]) < 5 or len(argv[1:]) % 2 != 1:
        print >> sys.stderr, 'Merge feature scores from multiple grammars'
        print >> sys.stderr, 'Word alignments in rules are the _union_ of all alignments for the rule (usually doesn\'t matter)'
        print >> sys.stderr, 'Usage: {0} outdir name1 gramdir1 name2 gramdir2 [name3 gramdir3 ...]'.format(argv[0])
        sys.exit(1)

    outdir = os.path.abspath(argv[1])
    if os.path.exists(outdir):
        print >> sys.stderr, '{0} exists, not overwriting'.format(outdir)
        sys.exit(1)
    os.mkdir(outdir)

    name = []
    gdir = []
    for i in range(2, len(argv), 2):
        name.append(argv[i])
        gdir.append(os.path.abspath(argv[i+1]))

    files = set([tuple(os.listdir(x)) for x in gdir])
    if len(files) != 1:
        print >> sys.stderr, 'Error: directories do not contain grammars for the same segments'
        sys.exit(1)
    files = files.pop()

    for f in sorted(files, cmp=lambda x,y: cmp(int(x.split('.')[2]), int(y.split('.')[2]))):
        print >> sys.stderr, f
        rules = {} # (X, src, tgt) -> (feats-list, align-set)
        for (gd, n) in zip(gdir, name):
            for line in gzip.open(os.path.join(gd, f)):
                tok = line.rstrip('\n').split('|||')
                key = (tok[0].strip(), tok[1].strip(), tok[2].strip())
                feats = tok[3].split()
                for i in range(len(feats)):
                    if '=' not in feats[i]:
                        feats[i] = 'phrase_{0}={1}'.format(i, feats[i])
                    feats[i] = '{0}_{1}'.format(n, feats[i])
                align = set(tok[4].split())
                if key not in rules:
                    rules[key] = [[], set()]
                entry = rules[key]
                for ft in feats:
                    entry[0].append(ft)
                entry[1] = entry[1].union(align)
        f_out = gzip.open(os.path.join(outdir, f), 'wb')
        for key in sorted(rules):
            entry = rules[key]
            print >> f_out, ' ||| '.join(key) + ' ||| ' + ' '.join(entry[0]) + ' ||| ' + ' '.join(sorted(entry[1]))
        f_out.close()

if __name__ == '__main__' : main(sys.argv)
