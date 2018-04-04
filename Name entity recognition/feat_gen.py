#!/bin/python
import os
from string import punctuation
import nltk

#############################
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def hasSpecial(inputString):
    match = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return not all([c in match for c in inputString])
#############################
corpus_list = []
filename_list = []
entity_dict = {}
sentence_postag = {}

def preprocess_corpus(train_sents):
    """Use the sentences to do whatever preprocessing you think is suitable,
    such as counts, keeping track of rare features/words to remove, matches to lexicons,
    loading files, and so on. Avoid doing any of this in token2features, since
    that will be called on every token of every sentence.

    Of course, this is an optional function.

    Note that you can also call token2features here to aggregate feature counts, etc.
    """

    for filename in os.listdir("./data/lexicon"):
        ll = set()
        with open("./data/lexicon/" + filename) as fp:
            for line in fp:
                word_list = line.split()
                for it in word_list:
                    ll.add(it)
                # ll.append(line)

        corpus_list.append(ll)
        filename_list.append(filename)




def token2features(sent, i, tags, add_neighs = True):
    """Compute the features of a token.

    All the features are boolean, i.e. they appear or they do not. For the token,
    you have to return a set of strings that represent the features that *fire*
    for the token. See the code below.

    The token is at position i, and the rest of the sentence is provided as well.
    Try to make this efficient, since it is called on every token.

    One thing to note is that it is only called once per token, i.e. we do not call
    this function in the inner loops of training. So if your training is slow, it's
    not because of how long it's taking to run this code. That said, if your number
    of features is quite large, that will cause slowdowns for sure.

    add_neighs is a parameter that allows us to use this function itself in order to
    recursively add the same features, as computed for the neighbors. Of course, we do
    not want to recurse on the neighbors again, and then it is set to False (see code).
    """
    ftrs = []
    # bias
    ftrs.append("BIAS")
    # position features
    if i == 0:
        ftrs.append("SENT_BEGIN")
    if i == len(sent)-1:
        ftrs.append("SENT_END")


    # the word itself
    word = unicode(sent[i])
    ftrs.append("WORD=" + word)
    ftrs.append("LCASE=" + word.lower())
    # some features of the word
    if word.isalnum():
        ftrs.append("IS_ALNUM")
    if word.isnumeric():
        ftrs.append("IS_NUMERIC")
    if word.isdigit():
        ftrs.append("IS_DIGIT")
    if word.isupper():
        ftrs.append("IS_UPPER")
    if word.islower():
        ftrs.append("IS_LOWER")
    #########################
    if len(word) > 8:
        ftrs.append("IS_LONGER.")
    if hasNumbers(word):
        ftrs.append("HAS_NUMBER")
    if hasSpecial(word):
        ftrs.append("HAS_SPECIAL")
    if word[0].upper():
        ftrs.append("FIRST_UPPER")
    elif any(x.isupper() for x in word):
        ftrs.append("INNER_UPPER")
    if word[0] in punctuation:
        ftrs.append("LEAD_SPECIAL")
    # 94 96 94 CURRENT SCORE UPPON

    if word[0] == "@":
        ftrs.append("TWITTER_TAG")
    if word[0] == "#":
        ftrs.append("HASHTAG")
    if word in nltk.corpus.stopwords.words("English"):
        ftrs.append("STOPWORDS")

        # Other features
    ftrs.append("LEN=" + str(len(word)))
    ftrs.append("CURRENT_TAG=" + tags[i][1])

    for m in range(len(corpus_list)):
        if sent[i] in corpus_list[m]:
            ftrs.append("IN_" + filename_list[m])



    # previous/next word feats
    if add_neighs:
        if i > 0:
            for pf in token2features(sent, i-1, tags, add_neighs = False):
                ftrs.append("PREV_" + pf)
            if sent[i - 1] == "the" or sent[i - 1] == "The":
                ftrs.append("PREV_THE");
        if i < len(sent)-1:
            for pf in token2features(sent, i+1, tags, add_neighs = False):
                ftrs.append("NEXT_" + pf)

    # return it!
    return ftrs

if __name__ == "__main__":
    sents = [
    [ "I", "love", "food" ]
    ]
    preprocess_corpus(sents)
    #sentence_postag = nltk.pos_tag(sents)

    for sent in sents:
        sentence_postag = nltk.pos_tag(sent)
        for i in xrange(len(sent)):
            print sent[i], ":", token2features(sent, i, sentence_postag)
