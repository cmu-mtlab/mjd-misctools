#!/usr/bin/env bash

for dir in moses qual-est text-processing ; do
  cd $dir ;
  ./compile.sh ;
  cd .. ;
done
