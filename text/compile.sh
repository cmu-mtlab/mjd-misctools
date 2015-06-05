#!/usr/bin/env bash

set -x

g++ -o ken-clean -licudata -licui18n -licuio -licule -liculx -licutest -licutu -licuuc ken-clean.cc

for j in *.java ; do javac -J-Xmx1G $j ; done
