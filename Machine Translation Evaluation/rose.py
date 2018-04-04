#!/usr/bin/env python
from __future__ import division
import argparse  # optparse is deprecated
from itertools import islice  # slicing for iterators
from nltk import ngrams
from sklearn.svm import SVR
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
import string
import nltk
import numpy as np


nums_content = "AGAIN AGO ALMOST ALREADY ALSO ALWAYS ANYWHERE BACK ELSE EVEN EVER EVERYWHERE FAR HENCE HERE HITHER HOW HOWEVER JUST NEAR NEARBY NEARLY NEVER NOT NOW NOWHERE OFTEN ONLY QUITE RATHER SOMETIMES SOMEWHERE SOON STILL THEN THENCE THERE THEREFORE THITHER THUS TODAY TOMORROW TOO UNDERNEATH VERY WHEN WHENCE WHERE WHITHER WHY YES YESTERDAY YET"
aliverb_content = "AM ARE AREN'T BE BEEN BEING CAN CAN'T COULD COULDN'T DID DIDN'T DO DOES DOESN'T DOING DONE DON'T GET GETS GETTING GOT HAD HADN'T HAS HASN'T HAVE HAVEN'T HAVING HE'D HE'LL HE'S I'D I'LL I'M IS I'VE ISN'T IT'S MAY MIGHT MUST MUSTN'T OUGHT OUGHTN'T SHALL SHAN'T SHE'D SHE'LL SHE'S SHOULD SHOULDN'T THAT'S THEY'D THEY'LL THEY'RE WAS WASN'T WE'D WE'LL WERE WE'RE WEREN'T WE'VE WILL WON'T WOULD WOULDN'T YOU'D YOU'LL YOU'RE YOU'VE"
conject_content ="ABOUT ABOVE AFTER ALONG ALTHOUGH AMONG AND AROUND AS AT BEFORE BELOW BENEATH BESIDE BETWEEN BEYOND BUT BY DOWN DURING EXCEPT FOR FROM IF IN INTO NEAR NOR OF OFF ON OR OUT OVER ROUND SINCE SO THAN THAT THOUGH THROUGH TILL TO TOWARDS UNDER UNLESS UNTIL UP WHEREAS WHILE WITH WITHIN WITHOUT"
numbers_context = "BILLION BILLIONTH EIGHT EIGHTEEN EIGHTEENTH EIGHTH EIGHTIETH EIGHTY ELEVEN ELEVENTH FIFTEEN FIFTEENTH FIFTH FIFTIETH FIFTY FIRST FIVE FORTIETH FORTY FOUR FOURTEEN FOURTEENTH FOURTH HUNDRED HUNDREDTH LAST MILLION MILLIONTH NEXT NINE NINETEEN NINETEENTH NINETIETH NINETY NINTH ONCE ONE SECOND SEVEN SEVENTEEN SEVENTEENTH SEVENTH SEVENTIETH SEVENTY SIX SIXTEEN SIXTEENTH SIXTH SIXTIETH SIXTY TEN TENTH THIRD THIRTEEN THIRTEENTH THIRTIETH THIRTY THOUSAND THOUSANDTH THREE THRICE TWELFTH TWELVE TWENTIETH TWENTY TWICE TWO"
all_content = "A ABOUT ABOVE AFTER AGAIN AGO ALL ALMOST ALONG ALREADY ALSO ALTHOUGH ALWAYS AM AMONG AN AND ANOTHER ANY ANYBODY ANYTHING ANYWHERE ARE AREN'T AROUND AS AT BACK ELSE BE BEEN BEFORE BEING BELOW BENEATH BESIDE BETWEEN BEYOND BILLION BILLIONTH BOTH EACH BUT BY CAN CAN'T COULD COULDN'T DID DIDN'T DO DOES DOESN'T DOING DONE DON'T DOWN DURING EIGHT EIGHTEEN EIGHTEENTH EIGHTH EIGHTIETH EIGHTY EITHER ELEVEN ELEVENTH ENOUGH EVEN EVER EVERY EVERYBODY EVERYONE EVERYTHING EVERYWHERE EXCEPT FAR FEW FEWER FIFTEEN FIFTEENTH FIFTH FIFTIETH FIFTY FIRST FIVE FOR FORTIETH FORTY FOUR FOURTEEN FOURTEENTH FOURTH HUNDRED FROM GET GETS GETTING GOT HAD HADN'T HAS HASN'T HAVE HAVEN'T HAVING HE HE'D HE'LL HENCE HER HERE HERS HERSELF HE'S HIM HIMSELF HIS HITHER HOW HOWEVER NEAR HUNDREDTH I I'D IF I'LL I'M IN INTO IS I'VE ISN'T IT ITS IT'S ITSELF JUST LAST LESS MANY ME MAY MIGHT MILLION MILLIONTH MINE MORE MOST MUCH MUST MUSTN'T MY MYSELF NEAR NEARBY NEARLY NEITHER NEVER NEXT NINE NINETEEN NINETEENTH NINETIETH NINETY NINTH NO NOBODY NONE NOONE NOTHING NOR NOT NOW NOWHERE OF OFF OFTEN ON OR ONCE ONE ONLY OTHER OTHERS OUGHT OUGHTN'T OUR OURS OURSELVES OUT OVER QUITE RATHER ROUND SECOND SEVEN SEVENTEEN SEVENTEENTH SEVENTH SEVENTIETH SEVENTY SHALL SHAN'T SHE'D SHE SHE'LL SHE'S SHOULD SHOULDN'T SINCE SIX SIXTEEN SIXTEENTH SIXTH SIXTIETH SIXTY SO SOME SOMEBODY SOMEONE SOMETHING SOMETIMES SOMEWHERE SOON STILL SUCH TEN TENTH THAN THAT THAT THAT'S THE THEIR THEIRS THEM THEMSELVES THESE THEN THENCE THERE THEREFORE THEY THEY'D THEY'LL THEY'RE THIRD THIRTEEN THIRTEENTH THIRTIETH THIRTY THIS THITHER THOSE THOUGH THOUSAND THOUSANDTH THREE THRICE THROUGH THUS TILL TO TOWARDS TODAY TOMORROW TOO TWELFTH TWELVE TWENTIETH TWENTY TWICE TWO UNDER UNDERNEATH UNLESS UNTIL UP US VERY WHEN WAS WASN'T WE WE'D WE'LL WERE WE'RE WEREN'T WE'VE WHAT WHENCE WHERE WHEREAS WHICH WHILE WHITHER WHO WHOM WHOSE WHY WILL WITH WITHIN WITHOUT WON'T WOULD WOULDN'T YES YESTERDAY YET YOU YOUR YOU'D YOU'LL YOU'RE YOURS YOURSELF YOURSELVES YOU'VE"


def read_files(data_file, answer_file, X, y):

    with open(data_file, 'r') as a, open(answer_file, 'r') as b:
        input1 = a.readline()
        input2 = b.readline()
        count = 0

        while len(input1) != 0 and len(input2) != 0:
            if count == 800:
                break
            count += 1
            # print input1 # input data file
            # print input2
            hhr = input1.split(' ||| ')
            h1 = hhr[0].strip()
            h2 = hhr[1].strip()
            ref = hhr[2].strip()
            #print type(h1)
            ans = int(input2.strip())
            rose(h1, h2, ref, ans, X, y)
            #print type(ans)
            #print count
            input1 = a.readline()
            input2 = b.readline()

    #print "AFTER"
    #print X
    #print y


#    plt.plot(X, y, color='navy')



def rose(h1, h2, ref, ans, X, y):
    #print len(ref.split())


    recall_list1 = []
    precision_list1 = []
    fscore_list1 = []

    recall_list2 = []
    precision_list2 = []
    fscore_list2 = []

    for n in range(1, 5):
        h1ngrams = ngrams(h1.split(), n)
        h2ngrams = ngrams(h2.split(), n)
        refngrams = ngrams(ref.split(), n)
        h1_list = list(h1ngrams)
        h2_list = list(h2ngrams)
        ref_list = list(refngrams)


        # print "++++++++++++"
        # print n
        # print h2
        # print h2_list
        # print len(h2_list)
        # print "************"

        # mactches1 = 0
        # for w in h1_list:
        #     if w in ref_list:
        #         mactches1 += 1

        matches1 = sum(1 for w in h1_list if w in ref_list)
        matches2 = sum(1 for w in h2_list if w in ref_list)

        # r = matches / len(ref)
        # p = matches / len(h)
        #one_f1 = 2 * one_matches1 / (len(ref) + len(h1))

        if len(ref_list) == 0:
            r1 = 0
            r2 = 0
            recall_list1.append(r1)
            recall_list2.append(r2)
        else:
            r1 = matches1 / len(ref_list)
            recall_list1.append(r1)
            r2 = matches2 / len(ref_list)
            recall_list2.append(r2)

        if len(h1_list) == 0:
            p1 = 0
        else:
            p1 = matches1 / len(h1_list)
        precision_list1.append(p1)
        if len(h2_list) == 0:
            p2 = 0
        else:
            p2 = matches2 / len(h2_list)
        precision_list2.append(p2)

        if len(h1_list) + len(ref_list) == 0:
            f1 = 0
        else:
            f1 = 2 * matches1 / (len(h1_list)+ len(ref_list))
        fscore_list1.append(f1)

        if len(h2_list) + len(ref_list) == 0:
            f2 = 0
        else:
            f2 = 2 * matches2 / (len(h2_list) + len(ref_list))
        fscore_list2.append(f2)

    word_count1 = abs(len(h1.split()) - len(ref.split())) / len(ref.split())
    word_count2 = abs(len(h2.split()) - len(ref.split())) / len(ref.split())

    punctuation_count1 = abs(sum(1 for w in h1 if w in string.punctuation) - sum(1 for w in ref if w in string.punctuation)) / len(ref.split())
    punctuation_count2 = abs(sum(1 for w in h2 if w in string.punctuation) - sum(1 for w in ref if w in string.punctuation)) / len(ref.split())

    ref_stopwords_count = 0
    for each in ref.split():
        if each.decode('utf-8') in stopwords.words('english'):
            ref_stopwords_count += 1
    h1_stopwords_count = 0
    h2_stopwords_count = 0

    for each in h1.split():
        if each.decode('utf-8') in stopwords.words('english'):
            h1_stopwords_count += 1

    for each in h2.split():
        if each.decode('utf-8') in stopwords.words('english'):
            h2_stopwords_count += 1
    function_count1 = abs(h1_stopwords_count - ref_stopwords_count) / len(ref.split())
    function_count2 = abs(h2_stopwords_count - ref_stopwords_count) / len(ref.split())
    #function_count1 = abs(sum(1 for w in h1 if w.lower().decode('utf-8') in stopwords.words('english')) - sum(1 for w in ref if w.lower().decode('utf-8') in stopwords.words('english'))) / len(ref)
    #function_count2 = abs(sum(1 for w in h2 if w.lower().decode('utf-8') in stopwords.words('english')) - sum(1 for w in ref if w.lower().decode('utf-8') in stopwords.words('english'))) / len(ref)

    #content_count1 =

    precision_average1 = float(sum(precision_list1)) / max(len(precision_list1), 1)
    #print sum(precision_list1)
    #print precision_average1
    precision_average2 = float(sum(precision_list2)) / max(len(precision_list2), 1)
    #print sum(precision_list2)
    #print precision_average2

    ## content word
    all_content = "A ABOUT ABOVE AFTER AGAIN AGO ALL ALMOST ALONG ALREADY ALSO ALTHOUGH ALWAYS AM AMONG AN AND ANOTHER ANY ANYBODY ANYTHING ANYWHERE ARE AREN'T AROUND AS AT BACK ELSE BE BEEN BEFORE BEING BELOW BENEATH BESIDE BETWEEN BEYOND BILLION BILLIONTH BOTH EACH BUT BY CAN CAN'T COULD COULDN'T DID DIDN'T DO DOES DOESN'T DOING DONE DON'T DOWN DURING EIGHT EIGHTEEN EIGHTEENTH EIGHTH EIGHTIETH EIGHTY EITHER ELEVEN ELEVENTH ENOUGH EVEN EVER EVERY EVERYBODY EVERYONE EVERYTHING EVERYWHERE EXCEPT FAR FEW FEWER FIFTEEN FIFTEENTH FIFTH FIFTIETH FIFTY FIRST FIVE FOR FORTIETH FORTY FOUR FOURTEEN FOURTEENTH FOURTH HUNDRED FROM GET GETS GETTING GOT HAD HADN'T HAS HASN'T HAVE HAVEN'T HAVING HE HE'D HE'LL HENCE HER HERE HERS HERSELF HE'S HIM HIMSELF HIS HITHER HOW HOWEVER NEAR HUNDREDTH I I'D IF I'LL I'M IN INTO IS I'VE ISN'T IT ITS IT'S ITSELF JUST LAST LESS MANY ME MAY MIGHT MILLION MILLIONTH MINE MORE MOST MUCH MUST MUSTN'T MY MYSELF NEAR NEARBY NEARLY NEITHER NEVER NEXT NINE NINETEEN NINETEENTH NINETIETH NINETY NINTH NO NOBODY NONE NOONE NOTHING NOR NOT NOW NOWHERE OF OFF OFTEN ON OR ONCE ONE ONLY OTHER OTHERS OUGHT OUGHTN'T OUR OURS OURSELVES OUT OVER QUITE RATHER ROUND SECOND SEVEN SEVENTEEN SEVENTEENTH SEVENTH SEVENTIETH SEVENTY SHALL SHAN'T SHE'D SHE SHE'LL SHE'S SHOULD SHOULDN'T SINCE SIX SIXTEEN SIXTEENTH SIXTH SIXTIETH SIXTY SO SOME SOMEBODY SOMEONE SOMETHING SOMETIMES SOMEWHERE SOON STILL SUCH TEN TENTH THAN THAT THAT THAT'S THE THEIR THEIRS THEM THEMSELVES THESE THEN THENCE THERE THEREFORE THEY THEY'D THEY'LL THEY'RE THIRD THIRTEEN THIRTEENTH THIRTIETH THIRTY THIS THITHER THOSE THOUGH THOUSAND THOUSANDTH THREE THRICE THROUGH THUS TILL TO TOWARDS TODAY TOMORROW TOO TWELFTH TWELVE TWENTIETH TWENTY TWICE TWO UNDER UNDERNEATH UNLESS UNTIL UP US VERY WHEN WAS WASN'T WE WE'D WE'LL WERE WE'RE WEREN'T WE'VE WHAT WHENCE WHERE WHEREAS WHICH WHILE WHITHER WHO WHOM WHOSE WHY WILL WITH WITHIN WITHOUT WON'T WOULD WOULDN'T YES YESTERDAY YET YOU YOUR YOU'D YOU'LL YOU'RE YOURS YOURSELF YOURSELVES YOU'VE".lower()
    all_content_list = all_content.strip().split(" ")
    content_set = set(all_content_list)

    ref_stem = []
    h1_stem = []
    h2_stem = []
    #ref_synonyms_set = set()

    #for w in ref:
    #    ref_stem.append(WordNetLemmatizer().lemmatize(w.lower().decode('utf-8')))
    for w in h1.split():
        h1_stem.append(WordNetLemmatizer().lemmatize(w.lower().decode('utf-8')))
    for w in h2.split():
        h2_stem.append(WordNetLemmatizer().lemmatize(w.lower().decode('utf-8')))
    h1_content_count = 0
    h2_content_count = 0

    for w in h1_stem:
        if w in content_set:
            h1_content_count += 1

    for w in h2_stem:
        if w in content_set:
            h2_content_count += 1

    h1_content_count = h1_content_count / len(ref.split())
    h2_content_count = h2_content_count / len(ref.split())

    # #####
    # chencherry = SmoothingFunction()
    # bleu_h1 = bleu([ref.strip().split()], h1.strip().split(), smoothing_function=chencherry.method1)
    # bleu_h2 = bleu([ref.strip().split()], h2.strip().split(), smoothing_function=chencherry.method1)
    #
    # #####


    #####pos tag
    ref_text = nltk.word_tokenize(ref)
    ref_pos_tag = nltk.pos_tag(ref_text)

    h1_text = nltk.word_tokenize(h1)
    h1_pos_tag = nltk.pos_tag(h1_text)

    h2_text = nltk.word_tokenize(h2)
    h2_pos_tag = nltk.pos_tag(h2_text)
    # print ref_pos_tag
    # print h1_pos_tag
    # print h2_pos_tag

    count_pos_h1 = 0
    for w in h1_pos_tag:
        if w in ref_pos_tag:
            count_pos_h1 += 1
    #print count_pos_h1

    count_pos_h2 = 0
    for w in h2_pos_tag:
        if w in ref_pos_tag:
            count_pos_h2 += 1


    #print "yes"
    if len(ref_pos_tag) == 0:
        pos_tag_r1 = 0
        pos_tag_r2 = 0
        recall_list1.append(pos_tag_r1)
        recall_list2.append(pos_tag_r2)
    else:
        pos_tag_r1 = count_pos_h1 / len(ref_pos_tag)
        recall_list1.append(pos_tag_r1)
        pos_tag_r2 = count_pos_h2 / len(ref_pos_tag)
        recall_list2.append(pos_tag_r2)

    if len(h1_pos_tag) == 0:
        pos_tag_p1 = 0
    else:
        pos_tag_p1 = count_pos_h1 / len(h1_pos_tag)
    precision_list1.append(pos_tag_p1)
    if len(h2_pos_tag) == 0:
        pos_tag_p2 = 0
    else:
        pos_tag_p2 = count_pos_h2 / len(h2_pos_tag)
    precision_list2.append(pos_tag_p2)

    if len(h1_pos_tag) + len(ref_pos_tag) == 0:
        pos_tag_f1 = 0
    else:
        pos_tag_f1 = 2 * count_pos_h1 / (len(h1_pos_tag) + len(ref_pos_tag))
    fscore_list1.append(pos_tag_f1)

    if len(h2_pos_tag) + len(ref_pos_tag) == 0:
        pos_tag_f2 = 0
    else:
        pos_tag_f2 = 2 * count_pos_h2 / (len(h2_pos_tag) + len(ref_pos_tag))
    fscore_list2.append(pos_tag_f2)







    #######

    X1 = []
    X2 = []

    X1 = precision_list1 + recall_list1 + fscore_list1

    X1.append(precision_average1)
    X1.append(word_count1)
    X1.append(function_count1)
    X1.append(punctuation_count1)
    X1.append(h1_content_count)

    X2 = precision_list2 + recall_list2 + fscore_list2

    X2.append(precision_average2)
    X2.append(word_count2)
    X2.append(function_count2)
    X2.append(punctuation_count2)
    X2.append(h2_content_count)

    # print X1
    # print X2

    # print len(X1)
    # print len(X2)

    XX = []
    #XX = X1 + X2
    for i in range(len(X1)):
        XX.append(X1[i] - X2[i])

    #XX.append(0.3 * (bleu_h1 - bleu_h2))

    # X.append()
    # y.append(r1)
    # X.append(X2)
    # y.append(r2)
    X.append(XX)
    y.append(ans)

# def rose_main():
#     svr_lin = SVR(kernel='linear', C=1e3)
#     X = []
#     y = []
#     train_file = "./data/hyp1-hyp2-ref"
#     train_answer = "./data/dev.answers"
#     read_files(train_file, train_answer, X, y)
#     data = [[0.7, 0.4444444444444444, 0.25, 0.14285714285714285, 0.5833333333333334, 0.36363636363636365, 0.2,
#              0.1111111111111111, 0.6363636363636364, 0.4, 0.2222222222222222, 0.125, 0.3843253968253968,
#              0.16666666666666666,
#              0.16666666666666666, 0.0, 0.46153846153846156, 0.16666666666666666, 0.0, 0.0, 0.5, 0.18181818181818182,
#              0.0, 0.0, 0.48, 0.17391304347826086, 0.0, 0.0, 0.15705128205128205, 0.08333333333333333,
#              0.08333333333333333, 0.0]]
#     y = np.array(y)
#     yf = svr_lin.fit(np.array(X), np.array(y))
#     yes = yf.predict(np.array(data))
#     print type(yf)
#     print yes


def get_feature(h1, h2, ref):

    recall_list1 = []
    precision_list1 = []
    fscore_list1 = []

    recall_list2 = []
    precision_list2 = []
    fscore_list2 = []

    for n in range(1, 5):
        h1ngrams = ngrams(h1.split(), n)
        h2ngrams = ngrams(h2.split(), n)
        refngrams = ngrams(ref.split(), n)
        h1_list = list(h1ngrams)
        h2_list = list(h2ngrams)
        ref_list = list(refngrams)


        # print "++++++++++++"
        # print n
        # print h2
        # print h2_list
        # print len(h2_list)
        # print "************"

        # mactches1 = 0
        # for w in h1_list:
        #     if w in ref_list:
        #         mactches1 += 1

        matches1 = sum(1 for w in h1_list if w in ref_list)
        matches2 = sum(1 for w in h2_list if w in ref_list)

        # r = matches / len(ref)
        # p = matches / len(h)
        #one_f1 = 2 * one_matches1 / (len(ref) + len(h1))

        if len(ref_list) == 0:
            r1 = 0
            r2 = 0
            recall_list1.append(r1)
            recall_list2.append(r2)
        else:
            r1 = matches1 / len(ref_list)
            recall_list1.append(r1)
            r2 = matches2 / len(ref_list)
            recall_list2.append(r2)

        if len(h1_list) == 0:
            p1 = 0
        else:
            p1 = matches1 / len(h1_list)
        precision_list1.append(p1)
        if len(h2_list) == 0:
            p2 = 0
        else:
            p2 = matches2 / len(h2_list)
        precision_list2.append(p2)

        if len(h1_list) + len(ref_list) == 0:
            f1 = 0
        else:
            f1 = 2 * matches1 / (len(h1_list)+ len(ref_list))
        fscore_list1.append(f1)

        if len(h2_list) + len(ref_list) == 0:
            f2 = 0
        else:
            f2 = 2 * matches2 / (len(h2_list) + len(ref_list))
        fscore_list2.append(f2)

    word_count1 = abs(len(h1.split()) - len(ref.split())) / len(ref.split())
    word_count2 = abs(len(h2.split()) - len(ref.split())) / len(ref.split())

    punctuation_count1 = abs(sum(1 for w in h1 if w in string.punctuation) - sum(1 for w in ref if w in string.punctuation)) / len(ref.split())
    punctuation_count2 = abs(sum(1 for w in h2 if w in string.punctuation) - sum(1 for w in ref if w in string.punctuation)) / len(ref.split())

    ref_stopwords_count = 0
    for each in ref.split():
        if each.decode('utf-8') in stopwords.words('english'):
            ref_stopwords_count += 1
    h1_stopwords_count = 0
    h2_stopwords_count = 0

    for each in h1.split():
        if each.decode('utf-8') in stopwords.words('english'):
            h1_stopwords_count += 1

    for each in h2.split():
        if each.decode('utf-8') in stopwords.words('english'):
            h2_stopwords_count += 1
    function_count1 = abs(h1_stopwords_count - ref_stopwords_count) / len(ref.split())
    function_count2 = abs(h2_stopwords_count - ref_stopwords_count) / len(ref.split())
    #function_count1 = abs(sum(1 for w in h1 if w.lower().decode('utf-8') in stopwords.words('english')) - sum(1 for w in ref if w.lower().decode('utf-8') in stopwords.words('english'))) / len(ref)
    #function_count2 = abs(sum(1 for w in h2 if w.lower().decode('utf-8') in stopwords.words('english')) - sum(1 for w in ref if w.lower().decode('utf-8') in stopwords.words('english'))) / len(ref)

    #content_count1 =

    precision_average1 = float(sum(precision_list1)) / max(len(precision_list1), 1)
    #print sum(precision_list1)
    #print precision_average1
    precision_average2 = float(sum(precision_list2)) / max(len(precision_list2), 1)
    #print sum(precision_list2)
    #print precision_average2

    #####
    # chencherry = SmoothingFunction()
    # bleu_h1 = bleu([ref.strip().split()], h1.strip().split(), smoothing_function=chencherry.method1)
    # bleu_h2 = bleu([ref.strip().split()], h2.strip().split(), smoothing_function=chencherry.method1)

    ## content word
    all_content = "A ABOUT ABOVE AFTER AGAIN AGO ALL ALMOST ALONG ALREADY ALSO ALTHOUGH ALWAYS AM AMONG AN AND ANOTHER ANY ANYBODY ANYTHING ANYWHERE ARE AREN'T AROUND AS AT BACK ELSE BE BEEN BEFORE BEING BELOW BENEATH BESIDE BETWEEN BEYOND BILLION BILLIONTH BOTH EACH BUT BY CAN CAN'T COULD COULDN'T DID DIDN'T DO DOES DOESN'T DOING DONE DON'T DOWN DURING EIGHT EIGHTEEN EIGHTEENTH EIGHTH EIGHTIETH EIGHTY EITHER ELEVEN ELEVENTH ENOUGH EVEN EVER EVERY EVERYBODY EVERYONE EVERYTHING EVERYWHERE EXCEPT FAR FEW FEWER FIFTEEN FIFTEENTH FIFTH FIFTIETH FIFTY FIRST FIVE FOR FORTIETH FORTY FOUR FOURTEEN FOURTEENTH FOURTH HUNDRED FROM GET GETS GETTING GOT HAD HADN'T HAS HASN'T HAVE HAVEN'T HAVING HE HE'D HE'LL HENCE HER HERE HERS HERSELF HE'S HIM HIMSELF HIS HITHER HOW HOWEVER NEAR HUNDREDTH I I'D IF I'LL I'M IN INTO IS I'VE ISN'T IT ITS IT'S ITSELF JUST LAST LESS MANY ME MAY MIGHT MILLION MILLIONTH MINE MORE MOST MUCH MUST MUSTN'T MY MYSELF NEAR NEARBY NEARLY NEITHER NEVER NEXT NINE NINETEEN NINETEENTH NINETIETH NINETY NINTH NO NOBODY NONE NOONE NOTHING NOR NOT NOW NOWHERE OF OFF OFTEN ON OR ONCE ONE ONLY OTHER OTHERS OUGHT OUGHTN'T OUR OURS OURSELVES OUT OVER QUITE RATHER ROUND SECOND SEVEN SEVENTEEN SEVENTEENTH SEVENTH SEVENTIETH SEVENTY SHALL SHAN'T SHE'D SHE SHE'LL SHE'S SHOULD SHOULDN'T SINCE SIX SIXTEEN SIXTEENTH SIXTH SIXTIETH SIXTY SO SOME SOMEBODY SOMEONE SOMETHING SOMETIMES SOMEWHERE SOON STILL SUCH TEN TENTH THAN THAT THAT THAT'S THE THEIR THEIRS THEM THEMSELVES THESE THEN THENCE THERE THEREFORE THEY THEY'D THEY'LL THEY'RE THIRD THIRTEEN THIRTEENTH THIRTIETH THIRTY THIS THITHER THOSE THOUGH THOUSAND THOUSANDTH THREE THRICE THROUGH THUS TILL TO TOWARDS TODAY TOMORROW TOO TWELFTH TWELVE TWENTIETH TWENTY TWICE TWO UNDER UNDERNEATH UNLESS UNTIL UP US VERY WHEN WAS WASN'T WE WE'D WE'LL WERE WE'RE WEREN'T WE'VE WHAT WHENCE WHERE WHEREAS WHICH WHILE WHITHER WHO WHOM WHOSE WHY WILL WITH WITHIN WITHOUT WON'T WOULD WOULDN'T YES YESTERDAY YET YOU YOUR YOU'D YOU'LL YOU'RE YOURS YOURSELF YOURSELVES YOU'VE".lower()
    all_content_list = all_content.strip().split(" ")
    content_set = set(all_content_list)

    ref_stem = []
    h1_stem = []
    h2_stem = []
    # ref_synonyms_set = set()

    # for w in ref:
    #    ref_stem.append(WordNetLemmatizer().lemmatize(w.lower().decode('utf-8')))
    for w in h1.split():
        h1_stem.append(WordNetLemmatizer().lemmatize(w.lower().decode('utf-8')))
    for w in h2.split():
        h2_stem.append(WordNetLemmatizer().lemmatize(w.lower().decode('utf-8')))
    h1_content_count = 0
    h2_content_count = 0

    for w in h1_stem:
        if w in content_set:
            h1_content_count += 1

    for w in h2_stem:
        if w in content_set:
            h2_content_count += 1

    h1_content_count = h1_content_count / len(ref.split())
    h2_content_count = h2_content_count / len(ref.split())

    #####pos tag
    ref_text = nltk.word_tokenize(ref.decode('utf-8'))
    ref_pos_tag = nltk.pos_tag(ref_text)

    h1_text = nltk.word_tokenize(h1.decode('utf-8'))
    h1_pos_tag = nltk.pos_tag(h1_text)

    h2_text = nltk.word_tokenize(h2.decode('utf-8'))
    h2_pos_tag = nltk.pos_tag(h2_text)
    # print ref_pos_tag
    # print h1_pos_tag
    # print h2_pos_tag

    count_pos_h1 = 0
    for w in h1_pos_tag:
        if w in ref_pos_tag:
            count_pos_h1 += 1
    # print count_pos_h1

    count_pos_h2 = 0
    for w in h2_pos_tag:
        if w in ref_pos_tag:
            count_pos_h2 += 1

    # print "yes"
    if len(ref_pos_tag) == 0:
        pos_tag_r1 = 0
        pos_tag_r2 = 0
        recall_list1.append(pos_tag_r1)
        recall_list2.append(pos_tag_r2)
    else:
        pos_tag_r1 = count_pos_h1 / len(ref_pos_tag)
        recall_list1.append(pos_tag_r1)
        pos_tag_r2 = count_pos_h2 / len(ref_pos_tag)
        recall_list2.append(pos_tag_r2)

    if len(h1_pos_tag) == 0:
        pos_tag_p1 = 0
    else:
        pos_tag_p1 = count_pos_h1 / len(h1_pos_tag)
    precision_list1.append(pos_tag_p1)
    if len(h2_pos_tag) == 0:
        pos_tag_p2 = 0
    else:
        pos_tag_p2 = count_pos_h2 / len(h2_pos_tag)
    precision_list2.append(pos_tag_p2)

    if len(h1_pos_tag) + len(ref_pos_tag) == 0:
        pos_tag_f1 = 0
    else:
        pos_tag_f1 = 2 * count_pos_h1 / (len(h1_pos_tag) + len(ref_pos_tag))
    fscore_list1.append(pos_tag_f1)

    if len(h2_pos_tag) + len(ref_pos_tag) == 0:
        pos_tag_f2 = 0
    else:
        pos_tag_f2 = 2 * count_pos_h2 / (len(h2_pos_tag) + len(ref_pos_tag))
    fscore_list2.append(pos_tag_f2)

    X1 = []
    X2 = []

    X1 = precision_list1 + recall_list1 + fscore_list1

    X1.append(precision_average1)
    X1.append(word_count1)
    X1.append(function_count1)
    X1.append(punctuation_count1)
    X1.append(h1_content_count)

    X2 = precision_list2 + recall_list2 + fscore_list2

    X2.append(precision_average2)
    X2.append(word_count2)
    X2.append(function_count2)
    X2.append(punctuation_count2)
    X2.append(h2_content_count)




    XX = []
    # XX = X1 + X2
    for i in range(len(X1)):
        XX.append(X1[i] - X2[i])

    #XX.append(bleu_h1 - bleu_h2)

    #XX.append(0.3 * (bleu_h1 - bleu_h2))

    return [XX]

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
    # svm
    svr_lin = SVR(kernel='linear', C=1e3)
    X = []
    y = []
    train_file = "./data/hyp1-hyp2-ref"
    train_answer = "./data/dev.answers"
    read_files(train_file, train_answer, X, y)
    y = np.array(y)
    yf = svr_lin.fit(np.array(X), np.array(y))
    fsvm = open("svm_resumlt.txt", "w")

    count = 0
    # note: the -n option does not work in the original code
    for h1, h2, ref in islice(sentences(), opts.num_sentences):
        count += 1
        if  count == 56652:
            break
        #print count
        #print type(h1)
        #print type(ref)
        #rset = set(ref)
        h1_str = string.join(h1, " ")
        h2_str = string.join(h2, " ")
        ref_str = string.join(ref, " ")
        data = get_feature(h1_str.strip(), h2_str.strip(), ref_str.strip())
        yes = yf.predict(np.array(data))
        fsvm.write(str(yes) + "\n")


        h1_match = 0
        h2_match = 0
        if yes >= 0.1:
            h1_match = 1
            h2_match = -1
        elif yes <= -0.1:
            h1_match = -1
            h2_match = 1
        else:
            h1_match = h2_match = 0

        print(1 if h1_match > h2_match else  # \begin{cases}
              (0 if h1_match == h2_match
               else -1))  # \end{cases}
    fsvm.close()


# convention to allow import of this file as a module
if __name__ == '__main__':
    main()
    #print "Yes"

    # n_samples, n_features = 10, 5
    # np.random.seed(0)
    # y = np.random.randn(n_samples)
    # print type(y)
    # X = np.random.randn(n_samples, n_features)
    # print type(X)
    #
    # l1 = [[1,2], [2,3,5]]
    # my = np.array(l1)
    #
    # nd = np.ndarray((2,), buffer=my)
    # print type(my)
    #read_files("./data/hyp1-hyp2-ref", "./data/dev.answers")


    # h1 = "Republican leaders justify its policy necessary to combat electoral fraud."
    # h2 = "Republican leaders justify its policy of necessity in the fight against electoral fraud."
    # ref = "Republican leaders justified their policy by the need to combat electoral fraud."
    # X = []
    # y = []
    # rose(h1, h2, ref, 1, X, y)
    # print X
    # print y





    # Israeli officials are responsible for airport security
    # Israeli officials responsible of airport safety
    # ref = ['Israeli', 'officials', 'are', 'responsible', 'for', 'airport', 'security']
    # h = ['Israeli', 'officials', 'responsible', 'of', 'airport', 'safety']
    #
    # print meteor(h, ref)
    #
    #
    # m =  sum (1 for w in h if w in ref)
