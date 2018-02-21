#!/usr/bin/env python
import argparse
import sys
import codecs
if sys.version_info[0] == 2:
  from itertools import izip
else:
  izip = zip
from collections import defaultdict as dd
import re
import os.path
import gzip
import tempfile
import shutil
import atexit

# Use word_tokenize to split raw text into words
from string import punctuation

import nltk
from nltk.tokenize import word_tokenize

scriptdir = os.path.dirname(os.path.abspath(__file__))

reader = codecs.getreader('utf8')
writer = codecs.getwriter('utf8')

def prepfile(fh, code):
  if type(fh) is str:
    fh = open(fh, code)
  ret = gzip.open(fh.name, code if code.endswith("t") else code+"t") if fh.name.endswith(".gz") else fh
  if sys.version_info[0] == 2:
    if code.startswith('r'):
      ret = reader(fh)
    elif code.startswith('w'):
      ret = writer(fh)
    else:
      sys.stderr.write("I didn't understand code "+code+"\n")
      sys.exit(1)
  return ret

def addonoffarg(parser, arg, dest=None, default=True, help="TODO"):
  ''' add the switches --arg and --no-arg that set parser.arg to true/false, respectively'''
  group = parser.add_mutually_exclusive_group()
  dest = arg if dest is None else dest
  group.add_argument('--%s' % arg, dest=dest, action='store_true', default=default, help=help)
  group.add_argument('--no-%s' % arg, dest=dest, action='store_false', default=default, help="See --%s" % arg)



class LimerickDetector:

    def __init__(self):
        """
        Initializes the object to have a pronunciation dictionary available
        """
        self._pronunciations = nltk.corpus.cmudict.dict()

        consonant_list = ['B', 'CH', 'D', 'DH', 'F', 'G', 'HH', 'JH', 'K', 'L', 'M', 'N', 'NG', 'P', 'R', 'S', 'SH', 'T', 'TH', 'V', 'W', 'Y', 'Z', 'ZH']
        self.consonant_set = set(consonant_list)



    def num_syllables(self, word):
        """
        Returns the number of syllables in a word.  If there's more than one
        pronunciation, take the shorter one.  If there is no entry in the
        dictionary, return 1.
        """

        # TODO: provide an implementation!

        word = word.lower()
        word = filter(str.isalpha, word)
        #print word


        if word in self._pronunciations:
            least = 100
            # li = []
            for i in range(0, len(self._pronunciations[word])):
                li = self._pronunciations[word][i]
                c1 = 0

                for i in range(0, len(li)):
                    for c in li[i]:
                        if c.isdigit():
                            c1 += 1
                            break

                if c1 < least:
                    least = c1
            return least
        else:
            return 1

    def get_compare_sublist(self, pron_list, consonant_set):
        if pron_list[0] not in consonant_set:
            return pron_list
        else:
            start_index = 0
            for i in range(0, len(pron_list)):
                if pron_list[i] not in consonant_set:
                    start_index = i
                    break

            return [pron_list[i] for i in range(start_index, len(pron_list))]

    def rhymes(self, a, b):


        """
        Returns True if two words (represented as lower-case strings) rhyme,
        False otherwise.
        """

        # TODO: provide an implementation!
        #d = nltk.corpus.cmudict.dict()
        #word1 = 'eye'
        #word2 = 'die'
        #print d[word1]
        #print d[word2]

        '''
        consonant_list = ['B', 'CH', 'D', 'DH', 'F', 'G', 'HH', 'JH', 'K', 'L', 'M', 'N', 'NG', 'P', 'R', 'S', 'SH',
                          'T',
                          'TH', 'V', 'W', 'Y', 'Z', 'ZH']
        print len(consonant_list)

        consonant_set = set(consonant_list)
        '''

        a = a.lower()
        a = filter(str.isalpha, a)

        b = b.lower()
        b = filter(str.isalpha, b)

        all_possible1 = []
        all_possible2 = []

        for i in range(len(self._pronunciations[a])):
            all_possible1.append(self.get_compare_sublist(self._pronunciations[a][i], self.consonant_set))

        for i in range(len(self._pronunciations[b])):
            all_possible2.append(self.get_compare_sublist(self._pronunciations[b][i], self.consonant_set))

        #print all_possible1
        #print all_possible2

        for i in range(len(all_possible1)):
            for j in range(len(all_possible2)):
                if len(all_possible1[i]) == len(all_possible2[j]):
                    if all_possible1[i] == all_possible2[j]:
                        return True
                else:
                    if len(all_possible1[i]) < len(all_possible2[j]):
                        shorter = all_possible1[i]
                        longer = all_possible2[j]
                    else:
                        shorter = all_possible2[j]
                        longer = all_possible1[i]

                    flag = True
                    margin = len(longer) - len(shorter)
                    for com in range(len(shorter) - 1, -1, -1):
                        if shorter[com] != longer[com + margin]:
                            #print '^^^^^^^^^^^^^^^^^^'
                            #print shorter[com]
                            #print longer[com]
                            #print '$$$$$$$$$$$$$$$$$$'
                            flag = False
                            break

                    if flag:
                        return True
                    

        return False

    def get_line_syllables_number(self, sentence):
        #line = sentence.split()
        line  = word_tokenize(sentence)
        newline = []

        for each in line:
            if each[0].isalpha():
                newline.append(each)

        line = newline
        #print line

        count = 0

        for i in range(len(line)):
            count += self.num_syllables(line[i])

        #print count
        return count

    def is_limerick(self, text):
        """
        Takes text where lines are separated by newline characters.  Returns
        True if the text is a limerick, False otherwise.

        A limerick is defined as a poem with the form AABBA, where the A lines
        rhyme with each other, the B lines rhyme with each other, and the A lines do not
        rhyme with the B lines.


        Additionally, the following syllable constraints should be observed:
          * No two A lines should differ in their number of syllables by more than two.
          * The B lines should differ in their number of syllables by no more than two.
          * Each of the B lines should have fewer syllables than each of the A lines.
          * No line should have fewer than 4 syllables

        (English professors may disagree with this definition, but that's what
        we're using here.)


        """
        # TODO: provide an implementation!

        sentences = text.split('\n')
        new_sentences = []

        ######$
        for each in sentences:
            if any(char.isalpha() for char in each):
                new_sentences.append(each)
        sentences = new_sentences


        #print 'len of sentencess:'
        #print len(sentences)
        #print sentences
        if len(sentences ) != 5:
            return False

        count_num = []
        #print sentences
        for i in range(len(sentences)):
            count_num.append(self.get_line_syllables_number(sentences[i]))

        #flag = True
        #print len(count_num)

        if abs(count_num[0] - count_num[1]) > 2 | abs(count_num[0] - count_num[4]) > 2 | abs(
                        count_num[1] - count_num[4]) > 2:
            #flag = False
            return False
        if abs(count_num[2] - count_num[3]) > 2:
            #flag = False
            return False

        fewest_a = min(count_num[0], min(count_num[1], count_num[4]))
        more_b = max(count_num[2], count_num[3])

        if more_b >= fewest_a:
            #flag = False
            return False

        for i in range(len(count_num)):
            if count_num[i] < 4:
                #flag = False
                return False

        #line0 = sentences[0].split()

        line0 = word_tokenize(sentences[0])
        newline0 = []

        for each in line0:
            if each[0].isalpha():
                newline0.append(each)

        line0 = newline0

        line1 = word_tokenize(sentences[1])
        newline1 = []

        for each in line1:
            if each[0].isalpha():
                newline1.append(each)

        line1 = newline1

        line2 = word_tokenize(sentences[2])
        newline2 = []

        for each in line2:
            if each[0].isalpha():
                newline2.append(each)

        line2 = newline2

        line3 = word_tokenize(sentences[3])
        newline3 = []

        for each in line3:
            if each[0].isalpha():
                newline3.append(each)

        line3 = newline3

        line4 = word_tokenize(sentences[4])
        newline4 = []

        for each in line4:
            if each[0].isalpha():
                newline4.append(each)

        line4 = newline4

        if not self.rhymes(line0[len(line0) - 1], line1[len(line1) - 1]):
            #flag = False
            return False
        if not self.rhymes(line0[len(line0) - 1], line4[len(line4) - 1]):
            #flag = False
            return False
        if not self.rhymes(line1[len(line1) - 1], line4[len(line4) - 1]):
            #flag = False
            return False

        if not self.rhymes(line2[len(line2) - 1], line3[len(line3) - 1]):
            #flag = False
            return False

        if self.rhymes(line0[len(line0) - 1], line2[len(line2) - 1]):
            #flag = False
            return False

        return True




# The code below should not need to be modified
def main():
  parser = argparse.ArgumentParser(description="limerick detector. Given a file containing a poem, indicate whether that poem is a limerick or not",
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  addonoffarg(parser, 'debug', help="debug mode", default=False)
  parser.add_argument("--infile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input file")
  parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file")




  try:
    args = parser.parse_args()
  except IOError as msg:
    parser.error(str(msg))

  infile = prepfile(args.infile, 'r')
  outfile = prepfile(args.outfile, 'w')

  ld = LimerickDetector()
  lines = ''.join(infile.readlines())
  outfile.write("{}\n-----------\n{}\n".format(lines.strip(), ld.is_limerick(lines)))




if __name__ == '__main__':
  main()

