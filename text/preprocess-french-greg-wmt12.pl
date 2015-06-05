#!/usr/bin/env perl

use bytes;
use strict;


# Check for correct usage:
if($#ARGV != -1)
{
    print STDERR "Usage: cat <fr-file> | perl $0\n";
    print STDERR "Output goes to standard out.\n";
    exit;
}


# List of French pronouns:
my @Pronouns = ( "je", "j'", "tu", "il", "elle", "on",
				 "nous", "vous", "ils", "elles",
				 "me", "m'", "te", "t'",
				 "le", "l'", "la", "les", "lui", "leur",
				 "moi", "toi", "eux", "elles",
				 "ce", "c'", "ça", "ceci", "cela", "qui", "ci", "là" );
my $proRE = "";
foreach my $p (@Pronouns) { $proRE .= "($p)|"; }
$proRE = substr($proRE, 0, -1);

# Read input French on standard in and process lines:
while(my $line = <STDIN>)
{
    # Remove trailing hard return:
    chomp $line;

#   # Lowercase everything:
#	$line =~ tr/[A-Z]/[a-z]/;

	# Input regularization:
	$line =~ s/\xC2\x92/\'/g;        # curly apostrophes
	$line =~ s/\xE2\x80\x99/\'/g;    # curly apostrophes
	$line =~ s/\xEF\x80\xBD/\'/g;    # curly apostrophes
	$line =~ s/´/\'/g;               # curly apostrophes
	$line =~ s/\xC2\x93/\"/g;        # curly left quotes
	$line =~ s/\xE2\x80\x9C/\"/g;    # curly left quotes
	$line =~ s/\xC2\x94/\"/g;        # curly right quotes
	$line =~ s/\xE2\x80\x9D/\"/g;    # curly right quotes
	$line =~ s/″/\"/g;               # curly right quotes
	$line =~ s/\xC2\x85/ ... /g;     # ellipses
	$line =~ s/\xE2\x80\xA6/ ... /g; # ellipses
	$line =~ s/\xC2\x9C/oe/g;        # "oe" ligatures 
	$line =~ s/\xC2\x8C/Oe/g;        # "OE" ligatures
	$line =~ s/\xC2\xA0/ /g;         # non-breaking spaces
	$line =~ s/\xC2\xAB/\"/g;        # opening guillemets
	$line =~ s/\xC2\xBB/\"/g;        # closing guillemets
	$line =~ s/\xE2\x80\xA8/ /g;     # "line separator"
	$line =~ s/\xE2\x80\x94/ -- /g;  # em dash
	$line =~ s/\&amp;/&/g;           # HTML ampersand
	$line =~ s/\&quot;/\"/g;         # HTML quote

	# Some puncutuation preprocessing:
	$line =~ s/(\d+),(\d+)/\1\.\2/g;        # to English decimals -- conflicts with parser, but probably a good idea.
#	$line =~ s/ - / -- /g;                  # long dashes
	
	# Break off punctuation:
	$line =~ s/(,|:|;|!|\?|\%|\*|@|\`|\"|\(|\)|\[|\]|<|>|\{|\}|\\|\/)/ \1 /g;
	$line =~ s/(°|§|º)/ \1 /g;
	$line =~ s/\(/-LRB-/g;
	$line =~ s/\)/-RRB-/g;
	$line =~ s/(\D)\.(\D)\.(\D|$)/\1 \. \2 \. \3/g;
	$line =~ s/(\D)\.(\D|$)/\1 \. \2/g;
	$line =~ s/(\d)\.$/\1 \./;

	# Apostrophes break with known elisions:
	$line =~ s/(^| |-)((qu)|c|d|l|j|s|n|m|(lorsqu)|(puisqu))\'/\1\2\' /gi;

	# Exceptions:
	$line =~ s/(^| )m \. / M\. /gi;               # Titles
	$line =~ s/(^| )mme \. / Mme\. /gi;
	$line =~ s/(^| )mlle \. / Mlle\. /gi;
	$line =~ s/-\s+,/ - /g;                      # -, (after appositive)
	$line =~ s/(^| )([Nn]) ° / \2° /g;           # stylized number sign
	$line =~ s/(^| )([Ll])\' on( |$)/ \2\'on /g; # L'on (FTB guide p. 24)

	# Break apart subject-verb inversions that have hyphens:
	$line =~ s/([^ -]+)-t-($proRE)( |$)/\1 -t-\2 /gi;
	$line =~ s/(^| )([^ -]+)-($proRE)( |$)/\1\2 -\3 /gi;
	$line =~ s/(^| )([^ -]+)-($proRE)-/\1\2 -\3 -/gi;

	# Delete excess spaces:
    $line =~ s/\s+/ /g;
	$line =~ s/^\s+//;
	$line =~ s/\s+$//;

	print "$line\n";
}

