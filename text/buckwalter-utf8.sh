#!/usr/bin/env bash

STANFORD_PARSER_JAR="/home/mdenkows/stanford-parser-2012-01-06/stanford-parser.jar"
java -Xmx512M -cp $STANFORD_PARSER_JAR edu.stanford.nlp.international.arabic.Buckwalter
