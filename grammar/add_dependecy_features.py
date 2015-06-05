#!/usr/bin/env python

import collections
import gzip
import itertools
import sys

MAX_SIZE = 15
MAX_LEN = 5
MAX_NT = 2
longest_rule = 0

next_i = 0
smap_dict = {}
sunmap_dict = {}

def smap(s, i=None):
    if i:
        smap_dict[s] = i
        sunmap_dict[i] = s
        return
    global next_i
    i = smap_dict.get(s, next_i)
    if i == next_i:
        smap_dict[s] = i
        sunmap_dict[i] = s
        next_i += 1
    return i

def sunmap(i):
    return sunmap_dict[i]

# Preload non-terminals
smap_dict['[X,1]'] = -1
smap_dict['[X,2]'] = -1
smap_dict['[X]'] = -1
sunmap_dict[-1] = '[X]'

def get_phrases(words, g_phrases):
    global longest_rule

    w_len = len(words)
    phrases = set() # (fphrase, lex_i, lex_j)

    def extract(i, j, lex_i, lex_j, wc, ntc, syms):
        # Phrase extraction limits
        if j > (w_len - 1) or (j - i) + 1 > MAX_SIZE:
            return
        # Extend with word
        if wc + ntc < longest_rule:
            syms.append(words[j])
            f = tuple(syms)
            new_lex_i = min(lex_i, j)
            new_lex_j = max(lex_j, j)
            if f in g_phrases:
                phrases.add((f, i, j, new_lex_i, new_lex_j))
                #~print 'win: {}'.format(' '.join(sunmap(w) for w in f))
            #~else:
                #~print 'fail: {}'.format(' '.join(sunmap(w) for w in f))
            extract(i, j + 1, new_lex_i, new_lex_j, wc + 1, ntc, syms)
            syms.pop()
        # Extend with existing non-terminal
        if syms and syms[-1] < 0:
            # Don't re-extract the same phrase
            extract(i, j + 1, lex_i, lex_j, wc, ntc, syms)
        # Extend with new non-terminal
        if wc + ntc < longest_rule:
            if ntc < MAX_NT:  #not syms or (ntc < MAX_NT and syms[-1] >= 0):
                syms.append(-1)
                f = tuple(syms)
                if wc > 0 and f in g_phrases:
                    phrases.add((f, i, j, lex_i, lex_j))
                extract(i, j + 1, lex_i, lex_j, wc, ntc + 1, syms)
                syms.pop()

    # Try to extract phrases from every f index
    for i in range(w_len):
        extract(i, i, w_len, -1, 0, 0, [])

    return phrases

def get_deps(f):
    inp = open(f)
    while True:
        line = inp.next()
        if not line:
            break
        deps = {}
        while line != '\n':
            (i, _, _, _, _, _, j, _) = line.split()
            deps[int(i) - 1] = int(j) - 1
            line = inp.next()
        yield deps

def report(i):
    if i % 100000 == 0:
        sys.stderr.write('!')
    elif i % 10000 == 0:
        sys.stderr.write('.')

def main(argv):
    global longest_rule

    if len(argv[1:]) != 4:
        print >> sys.stderr, 'Usage: {} corpus corpus.parses grammar [f|e]'.format(argv[0])
        sys.exit(2)

    N = 0 if argv[4] == 'f' else 1

    # Load grammar
    g_rules = []
    g_phrases = set()
    sys.stderr.write('Reading grammar\n')
    lc = 0
    for line in gzip.open(argv[3]):
        lc += 1
        report(lc)
        g_rules.append(line.strip().split(' ||| '))
        p = tuple(smap(w) for w in g_rules[-1][N + 1].split())
        longest_rule = max(longest_rule, len(p))
        g_phrases.add(p)
    sys.stderr.write('\n')
    print >> sys.stderr, 'Longest rule: {}'.format(longest_rule)

    scores = {}  # phrase -> scores

    corpus = open(argv[1])

    sys.stderr.write('Reading corpus and parses\n')
    lc = 0
    for (line, deps) in itertools.izip(corpus, get_deps(argv[2])):
        lc += 1
        report(lc)
        inp = [smap(w) for w in line.split()]
        phr = get_phrases(inp, g_phrases)
        for p in sorted(phr):
            missing = 0
            for i in range(p[1], p[2] + 1):
                link = deps[i]
                if link != -1 and not p[1] <= link <= p[2]:
                    missing += 1
            old = scores.get(p[0], 9999)
            scores[p[0]] = min(old, missing)
        #~break
    sys.stderr.write('\n')

    #~for ph in scores:
    #~    print ' '.join(sunmap(w) for w in ph), '|||', scores[ph]

    #~print '-------------------------'

    for rule in g_rules:
        sc = scores.get(tuple(smap(w) for w in rule[N + 1].split()), 'NaN')
        rule[3] += ' MissingLink={}'.format(float(sc))
        print ' ||| '.join(rule)

if __name__ == '__main__':
    main(sys.argv)
