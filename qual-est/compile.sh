#!/usr/bin/env bash

set -x

for j in *.java ; do javac -J-Xmx1G $j ; done
