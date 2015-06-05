#!/usr/bin/env python

import codecs, locale, re, sys, unicodedata
from BeautifulSoup import UnicodeDammit

# TODO: add option to specify these to work with various tokenizers such as Moses
LRB = '-LRB-'
RRB = '-RRB-'
LQ = '``'
RQ = '\'\''

SRC_RQ = '"'
SRC_RRB = '-RRB-'

locale.setlocale(locale.LC_ALL, 'en_US')

def main(argv):
    
    if len(argv[1:]) != 0:
        print >> sys.stderr, 'usage: {0} < hyp > out'.format(argv[0])
        sys.exit(1)

    # Not used thus far
    #src_in = open(argv[1])

    for line in sys.stdin:

        # Get source properties
        #src = src_in.readline().split()
        #stop_quot = count_stop_quot(src, '.', SRC_RQ)
        #stop_rrb = count_stop_quot(src, '.', SRC_RRB)

        line = line.strip()

        # Full line corrections

        # Capitlize first letter
        line = upper_first(line)

        # Put together broken numbers
        line = fix_numbers(line)

        # Merge some common words
        line = americanize(line)

        # Word list corrections

        words = line.split()

        # Fix bad/mixed encodings
        fix_bad_encodings(words)

        # Fix quotes
        fix_pairs(words, LQ, RQ)

        # Fix parens (seems to break more than it helps)
        #fix_pairs(words, LRB, RRB)

        # Fix stop quote order to match source
        stop_quot = 1 # ignore source, use US english (wmt12)
        fix_stop_quot(words, '.', RQ, stop_quot)
        comm_quot = 1
        fix_stop_quot(words, ',', RQ, comm_quot)

        # Fix stop paren order to match source (seems to be a no-op)
        #fix_stop_quot(words, '.', RRB, stop_rrb)

        # Convert numbers to US format
        us_numbers(words)

        print ' '.join(words)

# Returns line
def upper_first(line):
    for i in range(len(line)):
        if line[i].isupper() or line[i].isdigit():
            return line
        if line[i].islower():
            return line[0:i] + line[i].upper() + line[i+1:]

# Returns line
def americanize(line):
    line = re.sub(r'( |^)per cent( |$)', r'\1percent\2', line)
    line = re.sub(r'( |^)can not( |$)', r'\1cannot\2', line)
    return line

# Modifies passed word list
def drop_accents(words, d):
    for i in range(len(words)):
        if words[i].islower():
            try:
                unicode(words[i], 'ascii')
            except:
                if words[i][0].islower():
                    words[i] = ''.join([c for c in unicodedata.normalize('NFD', unicode(words[i], 'utf-8')) if unicodedata.category(c) != 'Mn']).encode('utf-8')

# Modifies passed word list
def fix_bad_encodings(words):
    for i in range(len(words)):
        try:
            unicode(words[i], 'utf-8')
        except:
            w = UnicodeDammit(words[i])
            words[i] = w.unicode.encode('utf-8')

# pos = stop quot, neg = quot stop, 0 = none or mixed
def count_stop_quot(words, stop, quot):
    stop_quot = 0
    quot_stop = 0
    for i in range(len(words) - 1):
        if words[i] == stop and words[i + 1] == quot:
            stop_quot += 1
        if words[i] == quot and words[i + 1] == stop:
            quot_stop += 1
    return stop_quot - quot_stop

# Modifies passed words list
def fix_stop_quot(words, stop, quot, stop_quot):
    if stop_quot == 0:
        return
    for i in range(len(words) - 1):
        if words[i] == stop and words[i + 1] == quot and stop_quot < 0:
            words[i] = quot
            words[i + 1] = stop
        elif words[i] == quot and words[i + 1] == stop and stop_quot > 0:
            words[i] = stop
            words [i + 1] = quot

# Modifies passed list words
def fix_pairs(words, left, right):
    open = False
    for i in range(len(words)):
        if words[i] == left:
            if open:
                words[i] = right
                open = False
            else:
                open = True
        elif words[i] == right:
            if open:
                open = False
            else:
                words[i] = left
                open = True

# Modifies passed list words
def us_numbers(words):
    for i in range(len(words)):
        # Use commas
        s = words[i].replace('.000', ',000')
        try:
            n = int(s.replace(',000', '000'))
            # Format numbers 5 digits or greater, leave anything
            # less alone
            if n > 9999:
                words[i] = locale.format('%d', n, grouping=True)
        except:
            pass

# Returns line
def fix_numbers(line):
    oldline = None
    while line != oldline:
        oldline = line
        line = re.sub(r'(\d) (\d\d\d)', r'\1,\2', line)
    return line

if __name__ == '__main__' : main(sys.argv)

