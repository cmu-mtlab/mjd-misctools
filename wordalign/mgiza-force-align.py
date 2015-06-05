#!/usr/bin/env python

import glob, os, subprocess, sys

# Change as needed
mgiza_dir = '/lustre/group/avenue/mgizapp'

def main(argv):

    if len(argv[1:]) < 4:
        print >> sys.stderr, 'Force align with model 4'
        print >> sys.stderr, ''
        print >> sys.stderr, 'Usage: {0} corpus.src corpus.tgt mgiza-src-tgt-workdir workdir [cpus]'.format(argv[0])
        print >> sys.stderr, ''
        print >> sys.stderr, 'inputs/outputs use src-tgt naming convention, results in workdir, alignments merged to src-tgt.align'
        print >> sys.stderr, 'To align other direction, switch src and tgt'
        sys.exit(1)

    cpus = '4' if len(argv[1:]) < 5 else argv[5]
    
    run_mgiza(argv[1], argv[2], argv[3], argv[4], cpus)

def run_mgiza(src_f, tgt_f, mgiza_srctgt, work_dir, cpus):
    # Work dir
    if not os.path.exists(work_dir):
        os.mkdir(work_dir)
    # Log files for everything
    mgiza_out = open(os.path.join(work_dir, 'mgiza.out'), 'w')
    mgiza_err = open(os.path.join(work_dir, 'mgiza.err'), 'w')
    # Create snt files for input and augmented vcb files
    subprocess.Popen([
      os.path.join(mgiza_dir, 'scripts', 'plain2snt-hasvcb.py'),
      os.path.join(mgiza_srctgt, 'src.vcb'),
      os.path.join(mgiza_srctgt, 'tgt.vcb'),
      src_f,
      tgt_f,
      os.path.join(work_dir, 'src-tgt.snt'),
      os.path.join(work_dir, 'tgt-src.snt'),
      os.path.join(work_dir, 'src.vcb'),
      os.path.join(work_dir, 'tgt.vcb')
      ], stdout=mgiza_out, stderr=mgiza_err).wait()
    # Link word class files so MGiza can find them
    os.symlink(
      os.path.abspath(os.path.join(mgiza_srctgt, 'src.vcb.classes')),
      os.path.join(work_dir, 'src.vcb.classes'))
    os.symlink(
      os.path.abspath(os.path.join(mgiza_srctgt, 'tgt.vcb.classes')),
      os.path.join(work_dir, 'tgt.vcb.classes'))
    # Generate cooc files
    subprocess.Popen([
      os.path.join(mgiza_dir, 'src', 'snt2cooc'),
      os.path.join(work_dir, 'src-tgt.cooc'),
      os.path.join(work_dir, 'src.vcb'),
      os.path.join(work_dir, 'tgt.vcb'),
      os.path.join(work_dir, 'src-tgt.snt'),
    ], stdout=mgiza_out, stderr=mgiza_err).wait()
    # Run MGiza
    subprocess.Popen([
      os.path.join(mgiza_dir, 'src', 'mgiza'),
      os.path.join(mgiza_srctgt, 'src-tgt.gizacfg'),
      '-c', os.path.join(work_dir, 'src-tgt.snt'),
      '-o', os.path.join(work_dir, 'src-tgt'),
      '-s', os.path.join(work_dir, 'src.vcb'),
      '-t', os.path.join(work_dir, 'tgt.vcb'),
      '-m1', '0',
      '-m2', '0',
      '-mh', '0',
      '-coocurrence', os.path.join(work_dir, 'src-tgt.cooc'),
      '-restart', '11',
      '-previoust', os.path.join(mgiza_srctgt, 'src-tgt.t3.final'),
      '-previousa', os.path.join(mgiza_srctgt, 'src-tgt.a3.final'),
      '-previousd', os.path.join(mgiza_srctgt, 'src-tgt.d3.final'),
      '-previousn', os.path.join(mgiza_srctgt, 'src-tgt.n3.final'),
      '-previousd4', os.path.join(mgiza_srctgt, 'src-tgt.d4.final'),
      '-previousd42', os.path.join(mgiza_srctgt, 'src-tgt.D4.final'),
      '-m3', '0',
      '-m4', '1',
      '-ncpus', cpus,
    ], stdout=mgiza_out, stderr=mgiza_err).wait()
    # Merge alignments
    cmd_list = [os.path.join(mgiza_dir, 'scripts', 'merge_alignment.py')]
    for f in glob.glob(os.path.join(work_dir, 'src-tgt.A3.final.part*')):
        cmd_list.append(f)
    align_out = open(os.path.join(work_dir, 'src-tgt.align'), 'w')
    subprocess.Popen(cmd_list, stdout=align_out, stderr=mgiza_err).wait()
    align_out.close()
    # Cleanup
    mgiza_out.close()
    mgiza_err.close()

if __name__ == '__main__' : main(sys.argv)
