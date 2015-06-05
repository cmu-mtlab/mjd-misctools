#!/usr/bin/env python

import argparse, sys

def main(argv):

    arg = argparse.ArgumentParser(description='Format k-best into two corpus files')
    arg.add_argument('-m', metavar='metric', help='metric', default='bleu')
    arg.add_argument('-t', metavar='N', type=int, help='take top N %%', default=50)
    arg.add_argument('-b', metavar='N', type=int, help='take bottom N %%', default=50)
    arg.add_argument('kbest', metavar='in.kbest')
    arg.add_argument('good', metavar='out.good')
    arg.add_argument('bad', metavar='out.bad')
    a = arg.parse_args()

    kbest = open(a.kbest)
    good = open(a.good, 'w')
    bad = open(a.bad, 'w')
    mrank = a.m + 'Rank='
    top = a.t
    bot = a.b

    hyps = []
    i = '-1'
    for line in kbest:
        f = line.split('|||')
        if f[0].strip() != i:
            if i != '-1':
                hyps.sort(cmp=lambda x,y: cmp(x[0], y[0]))
                for i in range(0, int(0.01 * top * len(hyps))):
                    print >> good, hyps[i][1]
                for i in range(0, int(0.01 * bot * len(hyps))):
                    print >> bad, hyps[-(i+1)][1]
            hyps= []
            i = f[0].strip()
        j = f[-2].find(mrank) + len(mrank)
        k = f[-2].find(' ', j)
        r = int(f[-2][j:k])
        hyps.append((r, f[1].strip()))

    good.close()
    bad.close()

if __name__ == '__main__' : main(sys.argv)
