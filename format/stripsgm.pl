#!/usr/bin/perl -ln

print $1 if /<seg[^>]*>\s*(.*?)\s*<\/seg>/
