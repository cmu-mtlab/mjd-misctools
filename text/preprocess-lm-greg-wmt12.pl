#!/usr/bin/env perl

use strict;


# Check for correct usage:
if($#ARGV != 1)
{
    print STDERR "Usage: cat <in-file> | perl5 $0 <max-words> <max-word-length>\n";
	print STDERR "Parameters:\n";
	print STDERR "    <max-words> : Lines with more than this number of tokens will be removed\n";
	print STDERR "    <max-word-length> : Lines containing tokens longer than this many characters will be removed\n";
    print STDERR "Output goes to standard out\n";
    exit;
}

# Parameters:
my $MAX_LENGTH = $ARGV[0];
my $MAX_WORD_LENGTH = $ARGV[1];

# Process lines:
my $totalLines = 0;
my $keptLines = 0;
while(my $line = <STDIN>)
{
    # Remove trailing hard return:
    chomp $line;
	$totalLines++;

    # Delete HTML, blank lines, and long lines:
    next if(($line =~ /^</) ||
			($line =~ /^\s*$/) ||
			(NumTokens($line) > $MAX_LENGTH));

	# Delete lines with words that are too long:
	next if(LengthOfLongestWord($line) > $MAX_WORD_LENGTH);

	# If we survived, then print:
	print "$line\n";
	$keptLines++;
}
print STDERR "Kept $keptLines of $totalLines lines (" .
	($keptLines/$totalLines) . " percent)\n";


# NumTokens($string):
#    Returns the number of whitespace-separated tokens the $string contains.
sub NumTokens
{
	# Get parameters:
	my $string = shift @_;

	my @W = split(/\s+/, $string);
	return ($#W + 1);
}


# LengthOfLongestWord($string):
#    Returns the length, in characters, of the longest token in the $string.
sub LengthOfLongestWord
{
	# Get parameters:
	my $string = shift @_;

	my @W = split(/\s+/, $string);
	my $maxLength = 0;
	foreach my $w (@W)
	{
		my $length = length($w);
		if($length > $maxLength) { $maxLength = $length; }
	}
	return $maxLength;
}
