#!/usr/bin/env perl

# Reverses Stanford PTB-like tokenization.  Includes some rules by Greg Hanneman
# and some rules borrowed from the Moses detokenizer (Philipp Koehn, Josh Schroeder,
# and Ondrej Bojar)

use strict;
use utf8;

while (my $line = <STDIN>) {

    # Normalize spaces
    chomp $line;
    $line =~ s/\s+/ /g;

    # Unescape parser entities:
    $line =~ s/-LRB-/\(/g;
    $line =~ s/-RRB-/\)/g;
    $line =~ s/\\\//\//g;
    $line =~ s/\\\*/\*/g;

    # Merge punctuation by token to catch combinations/repetitions
    my @words = split(/ /, $line);
    $line = "";
    my $delim = " ";
    for (my $i = 0; $i < scalar(@words); $i++) {
        # Left-associating punctuation, some can repeat
        if ($words[$i] =~ /^([\.\?\!]+|[\,\:\;\%\)\]\>\}])$/) {
            $line .= $words[$i];
            $delim = " ";
        # Right-associating punctuation
        } elsif ($words[$i] =~ /^[\$\€\£\¥\(\[\<\{]$/) {
            $line .= $delim.$words[$i];
            $delim = "";
        # Hyphen (merge if between words)
        } elsif ($words[$i] eq "-") {
            if ($i > 0 && $i < scalar(@words) &&
              $words[$i-1] =~ /[\p{IsAlnum}]$/ &&
              $words[$i+1] =~ /^[\p{IsAlnum}]/) {
                $line .= $words[$i];
                $delim = "";
            } else {
                $line .= $delim.$words[$i];
                $delim = " ";
            }
        # Regular word
        } else {
            $line .= $delim.$words[$i];
            $delim = " ";
        }
    }

    # Additional non-overlapping merges
 
    # Contractions
    $line =~ s/ (n\'t|\'s|\'m|\'re|\'ve|\'ll|\'d)( |$)/$1$2/gi;

    # R & D -> R&D, AT & T -> AT&T, Leave Standard & Poor's
    $line =~ s/([A-Z0-9]+) & ([A-Z0-9]+)/$1&$2/g;

    # Times
    $line =~ s/( |^)(\d+): (\d+)( |$)/$1$2:$3$4/g;

    # Slashes
    $line =~ s/( |^)(\\|\/)( |$)/$2/g;

    # Clean up spaces
    $line =~ s/\s+/ /g;
    $line =~ s/^\s+//;
    $line =~ s/\s+$//;
    
	# Associate quotes
    $line =~ s/\`\` /\"/g;
    $line =~ s/ \'\'/\"/g;
    # Order matters here
    $line =~ s/ \'/'/g;
    $line =~ s/\` /'/g;
    # Mismatched quotes that are probably decoding errors
    $line =~ s/ (\`\`)$/\"/g;
    $line =~ s/^\'\' /\"/g;
    $line =~ s/(\`\`|\'\')/"/g;
    $line =~ s/`/'/g;
    $line =~ s/^' /'/g;

    print "$line\n";
}
