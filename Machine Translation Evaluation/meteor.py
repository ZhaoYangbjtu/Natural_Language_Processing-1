#!/usr/bin/env python
from __future__ import division
import argparse  # optparse is deprecated
from itertools import islice  # slicing for iterators
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn
import nltk
import string
from nltk import ngrams
import math

from scipy.stats.mstats import gmean


def bleu(h, ref):
    p_list = []
    for i in range(1,5):
        h_ngram_list = list(ngrams(h, i))
        ref_ngram_list = list(ngrams(ref, i))

        count = 0
        for w in h_ngram_list:
            if w in ref_ngram_list:
                count += 1
        if len(h_ngram_list) == 0:
            p = 1
        else:
            p = count / len(h_ngram_list)
        p_list.append(p)

    if p_list[0] * p_list[1] * p_list[2] * p_list[3] == 0:
        return 0
    geo_mean = gmean(p_list)
    BP = 1
    if len(h) > len(ref):
        BP = 1
    else:
        BP = math.exp(1 - len(ref) / len(h))

    return BP * geo_mean


def bleu2(h, ref):
    p_list = []
    for i in range(1,5):
        h_ngram_list = list(ngrams(h, i))
        ref_ngram_list = list(ngrams(ref, i))

        count = 0
        for w in h_ngram_list:
            if w in ref_ngram_list:
                count += 1
        if len(h_ngram_list) == 0:
            p = 1
        else:
            p = count / len(h_ngram_list)
        p_list.append(p)

    if p_list[0] * p_list[1] * p_list[2] * p_list[3] == 0:
        return 0
    geo_mean = gmean(p_list)
    BP = 1
    if len(h) > len(ref):
        BP = 1
    else:
        BP = math.exp(1 - len(ref) / len(h))

    return BP * geo_mean



def meteor_modify(h, ref):
    # pos_tag


    ref_str = string.join(ref, " ")
    ref_text = nltk.word_tokenize(ref_str.decode('utf-8'))
    ref = ref_text
    ref_pos_tag =  nltk.pos_tag(ref_text)
    dr = {}
    for each in ref_pos_tag:
        dr[each[0]] = each[1]
    #print dr

    h_str = string.join(h, " ")
    h_text = nltk.word_tokenize(h_str.decode('utf-8'))
    h = h_text
    h_pos_tag = nltk.pos_tag(h_text)
    dh = {}
    for each in h_pos_tag:
        dh[each[0]] = each[1]



    ref_stem = []
    h_stem = []
    ref_synonyms_set = set()

    for w in ref:
        ref_stem.append(WordNetLemmatizer().lemmatize(w.lower()))
    for w in h:
        h_stem.append(WordNetLemmatizer().lemmatize(w.lower()))


    h_set = set(h)
    ref_set = set(ref)

    ref_stem_set = set(ref_stem)
    h_stem_set = set(h_stem)

    matches = 0

    ref_synonyms_set = set()

    for w in ref_stem:
        for ss in wn.synsets(w):
            for each in ss.lemma_names():
                ref_synonyms_set.add(each)



    matches = 0
    for w in h_set:
        if dh[w] == "IN":
            matches += 0.2
        elif dh[w] == "CC":
            matches += 0.2
        elif w in ref_set:
            matches += 1
        elif w in ref_synonyms_set:
            matches += 0.7

    #matches = sum(1 for w in h_stem if w in ref_stem)


    r = matches / len(ref)
    p = matches / len(h)

    if r == 0 and p == 0:
        return 0
    return 0.8 * 10 * (p * r) / (1 * r + 9 * p)+ 0.2 * (bleu(h, ref))

def meteor(h, ref):
    matches = sum (1 for w in h if w in ref)
    r = matches / len(ref)
    p = matches / len(h)

    if r == 0 and p == 0:
        return 0

    # hypIndex = 0
    # chunk = 0
    # while hypIndex < len(h):
    #     if h[hypIndex] in ref:
    #         refIndex = ref.index(h[hypIndex])
    #         while refIndex < len(ref) and hypIndex < len(h) and h[hypIndex] == ref[refIndex]:
    #             hypIndex += 1
    #             refIndex += 1
    #         chunk += 1
    #     else:
    #         hypIndex += 1
    #
    # penalty = 0.5 * (chunk / matches)

    return 10 * (p * r) / (1 * r + 9 * p)


def main():
    parser = argparse.ArgumentParser(description='Evaluate translation hypotheses.')
    parser.add_argument('-i', '--input', default='data/hyp1-hyp2-ref',
                        help='input file (default data/hyp1-hyp2-ref)')
    parser.add_argument('-n', '--num_sentences', default=None, type=int,
                        help='Number of hypothesis pairs to evaluate')
    # note that if x == [1, 2, 3], then x[:None] == x[:] == x (copy); no need for sys.maxint
    opts = parser.parse_args()

    # we create a generator and avoid loading all sentences into a list
    def sentences():
        with open(opts.input) as f:
            for pair in f:
                yield [sentence.strip().split() for sentence in pair.split(' ||| ')]
    # note: the -n option does not work in the original code
    for h1, h2, ref in islice(sentences(), opts.num_sentences):

        h1_match = meteor_modify(h1, ref)
        h2_match = meteor_modify(h2, ref)

        print(1 if h1_match > h2_match else  # \begin{cases}
              (0 if h1_match == h2_match
               else -1))  # \end{cases}



# convention to allow import of this file as a module
if __name__ == '__main__':
    main()
