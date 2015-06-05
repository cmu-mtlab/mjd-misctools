#!/usr/bin/env perl

binmode(STDIN, ":utf8");
binmode(STDOUT, ":utf8");

$|++;

while (<>) {
    s/&lt;/</g;
    s/&gt;/>/g;
    s/&quot;/"/g;
    s/&apos;/'/g;
    s/&amp;/&/g; # & last
    print;
}

