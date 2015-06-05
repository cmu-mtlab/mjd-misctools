#!/usr/bin/env bash

if [ ! -e logs ] || [ ! -e scripts ] ; then
  echo "Please run from make-big-grammar workdir"
  exit 1
fi

for g in $(for f in *.grammar ; do echo "$(ls $f|grep gz|wc -l) $f" ; done | grep -v "^50" | cut -d' ' -f2 | cut -d '.' -f1) ; do qsub scripts/$g.sh ; done
