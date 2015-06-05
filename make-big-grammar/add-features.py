#!/usr/bin/env python

import gzip, os, sys

# sa-extract rules drop off significantly after 7
# weights are unstable after 5
MAX_WC = 6

# Hiero limit 2 nonterminals
MAX_XC = 2

# Up to 4 is ~97% of rules
MAX_UN = 5

def main(argv):

    if len(argv[1:]) != 2:
        print >> sys.stderr, 'Add discrete word, X, and rule count features'
        print >> sys.stderr, 'Usage: {0} gramdir new-gramdir'.format(argv[0])
        sys.exit(1)

    gd = os.path.abspath(argv[1])
    newgd = os.path.abspath(argv[2])

    if os.path.exists(newgd):
        print >> sys.stderr, '{0} exists, not overwriting'.format(newgd)
        sys.exit(1)
    os.mkdir(newgd)
    
    for f in sorted(os.listdir(gd), cmp=lambda x,y: cmp(int(x.split('.')[2]), int(y.split('.')[2]))):

        f_in = gzip.open(os.path.join(gd, f))
        f_out = gzip.open(os.path.join(newgd, f), 'w')
        # For the curious
        wc_c = [0] * (MAX_WC + 1)
        un_c = [0] * (MAX_UN + 1)
        
        for line in f_in:
            tok = line.rstrip('\n').split(' ||| ')
            # Name phrase features
            feats = tok[3].split()
            feats = [(x[0] + '=' + x[1]) for x in zip(['phrase_{0}'.format(i) for i in range(len(feats))], feats)]
            # Rule count
            feats.append('rule_count=1.0')
            # Word, X counts
            tgt = tok[2].split()
            wc = 0
            xc = 0
            for word in tgt:
                if word.startswith('[X,'):
                    xc += 1
                else:
                    wc += 1
            wc = min(wc, MAX_WC)
            xc = min(xc, MAX_XC)
            for i in range(1, wc):
                feats.append('wc_{0}=0.0'.format(i))
            feats.append('wc_{0}=1.0'.format(wc))
            for i in range(wc + 1, MAX_WC + 1):
                feats.append('wc_{0}=0.0'.format(i))
            for i in range(0, xc):
                feats.append('xc_{0}=0.0'.format(i))
            feats.append('xc_{0}=1.0'.format(xc))
            for i in range(xc + 1, MAX_XC + 1):
                feats.append('xc_{0}=0.0'.format(i))
            wc_c[wc] += 1 #dbg
            # Unaligned words
            tgt_al = set([int(x.split('-')[1]) for x in tok[4].split()])
            un = 0
            for i in range(len(tgt)):
                if i in tgt_al or tgt[i].startswith('[X,'):
                    break
                un += 1
            if un < len(tgt):
                for i in range(len(tgt) - 1, 0, -1):
                    if i in tgt_al or tgt[i].startswith('[X,'):
                        break
                    un += 1
            un = min(un, MAX_UN)
            un_c[un] += 1 #dbg
            for i in range(0, un):
                feats.append('un_{0}=0.0'.format(i))
            feats.append('un_{0}=1.0'.format(un))
            for i in range(un + 1, MAX_UN + 1):
                feats.append('un_{0}=0.0'.format(i))
            # Print
            tok[3] = ' '.join(feats)
            print >> f_out, ' ||| '.join(tok)
        f_out.close()
        # For the curious
        print >> sys.stderr, f, wc_c, un_c

if __name__ == '__main__' : main(sys.argv)
