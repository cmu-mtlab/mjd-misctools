#!/usr/bin/env bash

STANFORD_PARSER_JAR="/home/mdenkows/stanford-parser-2012-01-06/stanford-parser.jar"
java -Xmx666M -cp $STANFORD_PARSER_JAR edu.stanford.nlp.process.PTBTokenizer -preserveLines -options "normalizeSpace=true,americanize=true,normalizeCurrency=false,untokenizable=allKeep" <(sed -re 's/(<|>)/ \1 /g') | sed -e 's/\\\//\//g' | sed -e 's/\\\*/\*/g'
