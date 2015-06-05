#!/usr/bin/env perl

use strict;
use bytes;
#binmode(STDIN, ":utf8");
#binmode(STDOUT, ":utf8");


# Check for correct usage:
if($#ARGV != -1)
{
    print STDERR "Usage: cat <text> | perl $0\n";
    print STDERR "Output goes to standard out.\n";
    exit;
}

# Open standard input and process lines:
while(my $line = <STDIN>)
{
    # Remove trailing hard return:
    chomp $line;

    # Regularlize spaces:
    $line =~ s/\xC2\xA0/ /g;         # non-breaking space
    $line =~ s/\xE2\x80\x89/ /g;     # thin space
    $line =~ s/\xE2\x80\xA8/ /g;     # "line separator"
    $line =~ s/\xEF\xBF\xBD/ /g;     # "replacement character"

    # Regularize quotes:
    $line =~ s/\xC2\x92/\'/g;        # curly apostrophe
    $line =~ s/\xE2\x80\x99/\'/g;    # curly apostrophe
    $line =~ s/\xEF\x80\xBD/\'/g;    # curly apostrophe
    $line =~ s/\xC2\xB4/\'/g;        # curly apostrophe
    $line =~ s/\xE2\x80\x98/\'/g;    # curly single open quote
    $line =~ s/\xC2\x93/\"/g;        # curly left quote
    $line =~ s/\xE2\x80\x9C/\"/g;    # curly left quote
    $line =~ s/\xC2\x94/\"/g;        # curly right quote
    $line =~ s/\xE2\x80\x9D/\"/g;    # curly right quote
    $line =~ s/\xE2\x80\xB3/\"/g;    # curly right quote
    $line =~ s/\xC2\xAB/\"/g;        # opening guillemet
    $line =~ s/\xC2\xBB/\"/g;        # closing guillemet

    # Ridiculous Web quotes (news commentary and Giga-FrEn):
    $line =~ s/\xC3\xA2\xE2\x82\xACoe/\"/g;           # opening double quote
    $line =~ s/\xC3\xA2\xE2\x82\xAC\xC2\x9D/\"/g;     # closing double quote
    $line =~ s/\xC3\xA2\xE2\x82\xAC\xE2\x84\xA2/\'/g; # apostrophe

    # Regularize ellipses:
    $line =~ s/\xC2\x85/.../g;       # ellipsis
    $line =~ s/\xE2\x80\xA6/.../g;   # ellipsis

    # Regularize ligatures:
    $line =~ s/\xC2\x9C/oe/g;        # "oe" ligature 
    $line =~ s/\xC5\x93/oe/g;        # "oe" ligature 
    $line =~ s/\xC2\x8C/Oe/g;        # "OE" ligature
    $line =~ s/\xC5\x92/Oe/g;        # "OE" ligature
    $line =~ s/\xEF\xAC\x80/ff/g;    # "ff" ligature
    $line =~ s/\xEF\xAC\x81/fi/g;    # "fi" ligature
    $line =~ s/\xEF\xAC\x82/fl/g;    # "fl" ligature

    # Regularize HTML / XML escapes:
    $line =~ s/\&amp;/&/g;           # HTML ampersand
    $line =~ s/\&quot;/\"/g;         # HTML quote

    # Regularize other characters:
    $line =~ s/\xE2\x80\x91/-/g;     # non-breaking hyphen
    $line =~ s/\xE2\x80\x93/ -- /g;  # en dash
    $line =~ s/\xE2\x80\x94/ -- /g;  # em dash

    # Finally, collapse excess spaces:
    $line =~ s/\s+/ /g;

    print "$line\n";
}

