#!/usr/bin/env bash

if [[ $# != 1 ]] ; then
  echo "Usage: $0 grammar-dir"
  echo "Searches recursively, prints file names of bad grammars"
  exit 1
fi

for f in $(find $1 | egrep '\.gz$' | sort) ; do zcat $f | awk -F'\\|\\|\\|' "{if(NF!=5){print \"$f\"; exit}}" ; done
