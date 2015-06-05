#!/usr/bin/env python

import codecs, os, shutil, subprocess, sys, tempfile

mteval_pl = os.path.abspath(os.path.join(os.path.dirname(__file__), 'mteval-v13m.pl'))

def main(argv):
    
    if len(argv[1:]) < 2:
        print >> sys.stderr, 'Usage: {0} <hyp> <ref> [--no-norm] [--char]'.format(argv[0])
        print >> sys.stderr, 'Segment scores to stderr, final to stdout'
        sys.exit(1)
    
    work = tempfile.mkdtemp(prefix='bleu.')
    src_sgm = os.path.join(work, 'src.sgm')
    tst_sgm = os.path.join(work, 'tst.sgm')
    ref_sgm = os.path.join(work, 'ref.sgm')
    
    opts = argv[3:]

    cmd = ['perl', mteval_pl, '-s', src_sgm, '-t', tst_sgm, '-r', ref_sgm, '--metricsMATR']
    out = open(os.path.join(work, 'out'), 'w')
    err = open(os.path.join(work, 'err'), 'w')
    char = False
    for opt in opts:
        if opt == '--char':
            char = True
        else:
            cmd.append(opt)

    sgm(argv[2], src_sgm, 'srcset', char)
    sgm(argv[1], tst_sgm, 'tstset', char)
    sgm(argv[2], ref_sgm, 'refset', char)

    subprocess.Popen(cmd, stdout=out, stderr=err, cwd=work, env=os.environ.copy()).wait()
    
    for line in open(os.path.join(work, 'BLEU-seg.scr')):
        print >> sys.stderr, line.split()[-1]
        
    print open(os.path.join(work, 'BLEU-sys.scr')).readline().split()[-1]

    shutil.rmtree(work)
    
def sgm(f_in, f_out, f_type, char=False):
    i = codecs.open(f_in, 'r', 'utf-8')
    o = codecs.open(f_out, 'w', 'utf-8')
    s = 0
    print >> o, u'<{0} trglang="trg" setid="set" srclang="src">'.format(f_type)
    print >> o, u'<doc docid="doc" sysid="sys">'
    for line in i:
        s += 1
        if char:
            line = ' '.join([ch for ch in line if ch != ' '])
        print >> o, u'<seg id="{0}"> {1} </seg>'.format(s, line.strip())
    print >> o, u'</doc>'
    print >> o, u'</{0}>'.format(f_type)
    i.close()
    o.close()

if __name__ == '__main__' : main(sys.argv)
