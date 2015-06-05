#!/usr/bin/env python

from sys import argv
from collections import defaultdict

(a_src, a_tgt, b_src, b_tgt, c_src, c_tgt) = argv[1:]

as_in = open(a_src)
at_in = open(a_tgt)
bs_in = open(b_src)
bt_in = open(b_tgt)
cs_out = open(c_src, 'w')
ct_out = open(c_tgt, 'w')

a = defaultdict(int)

for src in as_in:
    tgt = at_in.readline()
    a[(src.strip(), tgt.strip())] += 1

for src in bs_in:
    tgt = bt_in.readline()
    x = (src.strip(), tgt.strip())
    if a[x] == 0:
        print >> cs_out, x[0]
        print >> ct_out, x[1]
    else:
        a[x] -= 1

cs_out.close()
ct_out.close()
