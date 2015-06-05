#!/usr/bin/env python

import codecs, sys

sys.stdin = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def main():

    vocab = set()

    for line in sys.stdin:
        for word in line.split():
            vocab.add(word)

    for word in sorted(vocab):
        print word

if __name__ == '__main__':
    main()
