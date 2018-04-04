import math
import time
import argparse
import sys
import codecs
import os.path
import gzip
import tempfile
import shutil
import atexit
if sys.version_info[0] == 2:
  from itertools import izip
else:
  izip = zip

from learngrammar import LearnGrammar
from bigfloat import bigfloat





class GrammarParser:
    two_array = []
    word_num = 0
    optimal = {}
    backpointer = {}
    len_list = []
    time_list = []

    def __init__(self):
        self.lg = LearnGrammar()
        #print "$$$$$$$$"
        #print training_name
        self.lg.write_PCFG_grammar()
        #self.local_grammar = induce_pcfg('TOP', self.lg.count_dict)


    # get the nonterminal from the start_dict
    def get_key_from_value(self, value):
        rl = []
        for key in self.lg.start_dict:
            if key + ' ' + value in self.lg.start_dict[key]:
                rl.append(key)

        if len(rl) == 0:
            rl.append("unk")

        return rl

    def viterbi_parse(self, sentence):
        before = time.time()
        input_list = sentence.split()
        self.word_num = len(input_list)
        # ignore 's for has
        apostrophe_dict = {'\'s' : 'is', '\'ve' : 'have', '\'ll' : 'will', '\'d' : 'would'}

        # initial start section
        self.optimal = {}
        self.backpointer = {}

        for i in range(self.word_num + 1):
            self.optimal[i] = {}
            self.backpointer[i] = {}
            for j in range(self.word_num + 1):
                self.optimal[i][j] = {}
                self.backpointer[i][j] = {}
                for rule in self.lg.start_dict:
                    self.optimal[i][j][rule] = 0
                    self.backpointer[i][j][rule] = []

        # deal with the unary--terminal part
        current_word = ''
        previous_word = ''
        for index in range(1, self.word_num + 1):
            if previous_word == '<unk>' and current_word == '<unk>':
                continue
            previous_word = current_word
            if input_list[index - 1] in apostrophe_dict:
                input_list[index - 1] = apostrophe_dict[input_list[index - 1]]
            if input_list[index - 1].lower() in self.lg.terminal_dict:
                current_word = input_list[index - 1].lower()
            else:
                current_word = '<unk>'
            #print current_word
            for key in self.lg.terminal_dict[current_word]:
                if self.lg.count_dict[key + ' ' + (current_word)] > self.optimal[index - 1][index][key]:
                    self.optimal[index - 1][index][key] = float(self.lg.count_dict[key + ' ' + current_word])
                    self.backpointer[index - 1][index][key].append(current_word)

        for length in range(2, self.word_num + 1):
            for m in range(0, self.word_num + 1 - length):
                n = m + length
                for k in range(m + 1, n):  # check end of range
                    for rule in self.lg.start_dict:
                        for right in self.lg.start_dict[rule]:
                            r = right.split()
                            if len(r) == 2:
                                continue
                            else:
                                p = float(self.lg.count_dict[right]) * float(self.optimal[m][k][r[1]]) * float(self.optimal[k][n][r[2]])
                                if p > self.optimal[m][n][rule]:
                                    self.optimal[m][n][rule] = p
                                    self.backpointer[m][n][rule] = []
                                    self.backpointer[m][n][rule].append(r[1])
                                    self.backpointer[m][n][rule].append(r[2])
                                    self.backpointer[m][n][rule].append(k)

        after = time.time()
        if not self.optimal[0][self.word_num]['TOP']:
            m = 0
            length = self.word_num
            n = m + length
            for k in range(m + 1, n):  # check end of range
                for rule in self.lg.start_dict:
                    for right in self.lg.start_dict[rule]:
                        r = right.split()
                        if len(r) == 2:
                            continue
                        else:
                            p = 1 * float(self.optimal[m][k][r[1]]) * float(
                                self.optimal[k][n][r[2]])
                            if p > self.optimal[m][n][rule]:
                                self.optimal[m][n][rule] = p
                                self.backpointer[m][n][rule] = []
                                self.backpointer[m][n][rule].append(r[1])
                                self.backpointer[m][n][rule].append(r[2])
                                self.backpointer[m][n][rule].append(k)
            #return 'Not Parse Successful'
        #else:
            #print str(math.log(self.word_num)) + ',' + str(math.log(after - before))
            #self.time_tuple.append(tuple([math.log(self.word_num),math.log(after - before)]))
        self.len_list.append(math.log(self.word_num, 10))
        self.time_list.append(math.log(after - before, 10))
        #print sentence
        if self.optimal[0][self.word_num]['TOP'] == 0:
            return 'Not Parse Successful'
        return str(math.log(self.optimal[0][self.word_num]['TOP'], 10))


    def print_tree(self, rule, i, j, back):
        if len(self.backpointer[i][j][rule]) == 1:
            sys.stdout.write('(' + rule + ' ' + back[i][j][rule][0] + ')')
        else:
            sys.stdout.write('(' + rule + ' ')
            self.print_tree(self.backpointer[i][j][rule][0], i, self.backpointer[i][j][rule][2], back)
            sys.stdout.write(' ')
            self.print_tree(self.backpointer[i][j][rule][1], self.backpointer[i][j][rule][2], j, back)
            sys.stdout.write(')')



    def parse(self, sentence):
        if len(sentence) == 0:
            return

        lengh = 1
        input_str = sentence.split()
        self.word_num = len(input_str)
        self.two_array = [[0 for x in range(self.word_num)] for y in range(self.word_num)]
        # nonterminal to terminal
        max_probability = -1
        backpointer = ''
        for index in range(len(input_str)):
            max_probability = -1
            backpointer = ''
            self.two_array[index][index] = {}
            rl= self.get_key_from_value(input_str[index])
            self.two_array[index][index]['key_probability'] = {}
            for each_key in rl:
                self.two_array[index][index]['key_probability'][each_key] = self.lg.count_dict[each_key + ' ' + input_str[index]]
                if float(self.lg.count_dict[each_key + ' ' + input_str[index]]) > float(max_probability):
                    max_probability = self.lg.count_dict[each_key + ' ' + input_str[index]]
                    backpointer = each_key + ' ' + input_str[index]
            #print type(max_probability)
            #print max_probability
            self.two_array[index][index]['_max_probability'] = bigfloat(float(max_probability))
            self.two_array[index][index]['_backpointer'] = backpointer
            self.two_array[index][index]['_left_position_x'] = index
            self.two_array[index][index]['_left_position_y'] = index
            self.two_array[index][index]['_right_position_x'] = None
            self.two_array[index][index]['_right_position_y'] = None


        # nonterminal to nonterminal
        for num in range(1, self.word_num):
            for i in range(0,self.word_num - num):
                self.two_array[i][i + num] = {}
                # x = i y = i + num
                # compare with --- |||
                self.two_array[i][i + num]['key_probability'] = {}
                #vertical - x
                v_dict = {}
                h_dict = {}
                max_probability = -1
                backpointer = ''
                left_position_x = None
                left_position_y = None
                right_position_x = None
                right_position_y = None

                for n in range(i + num - 1, i - 1, -1):
                    if self.two_array[i][n] != 0:
                        h_dict = self.two_array[i][n]['key_probability']
                        #for m in range(i + 1, i + num + 1):
                        # margin = i + num - (i + num - n) =
                        m = n + 1

                        print "################################"
                        print i
                        print num
                        print n
                        print m
                        print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"


                        if self.two_array[m][i + num] != 0:
                            v_dict = self.two_array[m][i + num]['key_probability']

                            for hk in h_dict:
                                for vk in v_dict:
                                    # first we got the rule_root of vk+hk, and pick the one with bigger value
                                    krl = self.get_key_from_value(hk + ' ' + vk)
                                    if krl[0] == 'unk':
                                        continue

                                    child_max_probability = -1
                                    child_rule = ''
                                    child_key = ''

                                    child_left_position_x = None
                                    child_left_position_y = None
                                    child_right_position_x = None
                                    child_right_position_y = None
                                    for k in krl:
                                        if (k + ' ' + hk + ' ' + vk) in self.lg.count_dict:
                                            if float(self.lg.count_dict[
                                                                                         k + ' ' + hk + ' ' + vk]) > child_max_probability:
                                                child_max_probability = self.lg.count_dict[k + ' ' + hk + ' ' + vk]
                                                child_rule = k + ' ' + hk + ' ' + vk
                                                child_key = k
                                                child_left_position_x = i
                                                child_left_position_y = n
                                                child_right_position_x = m
                                                child_right_position_y = i + num

                                    pro = float((child_max_probability)) * float(
                                        (h_dict[hk])) * float((v_dict[vk]))
                                    self.two_array[i][i + num]['key_probability'][k] = pro
                                    if pro > max_probability:
                                        max_probability = pro
                                        backpointer = child_rule
                                        left_position_x = child_left_position_x
                                        left_position_y = child_left_position_y
                                        right_position_x = child_right_position_x
                                        right_position_y = child_right_position_y

                self.two_array[i][i + num]['_max_probability'] = max_probability
                self.two_array[i][i + num]['_backpointer'] = backpointer
                self.two_array[i][i + num]['_left_position_x'] = left_position_x
                self.two_array[i][i + num]['_left_position_y'] = left_position_y
                self.two_array[i][i + num]['_right_position_x'] = right_position_x
                self.two_array[i][i + num]['_right_position_y'] = right_position_y

    def bfs(self, x, y):
        rstr = ''
        key_list = self.two_array[x][y]['_backpointer'].split()

        if len(key_list) == 2:
            rstr = rstr + key_list[0] + ' ' + key_list[1]
        else:
            rstr += key_list[0] + ' ( '
            rstr += self.bfs(self.two_array[x][y]['_left_position_x'],
                             self.two_array[x][y]['_left_position_y'])
            rstr += ' )'

            rstr += ' ( '
            rstr += self.bfs(self.two_array[x][y]['_right_position_x'],
                             self.two_array[x][y]['_right_position_y'])
            rstr += ' )'
        return rstr


    def backward(self):
        rstr = '( '
        key_list = self.two_array[0][self.word_num - 1]['_backpointer'].split()

        if len(key_list) == 2:
            rstr = rstr + key_list[0] + ' ' + key_list[1]
        else:
            print "key list len: " + str(len(key_list))
            rstr += key_list[0] + ' ( '
            rstr += self.bfs(self.two_array[0][self.word_num - 1]['_left_position_x'], self.two_array[0][self.word_num - 1]['_left_position_y'])
            rstr += ' )'

            rstr += ' ( '
            rstr += self.bfs(self.two_array[0][self.word_num - 1]['_right_position_x'], self.two_array[0][self.word_num - 1]['_right_position_y'])
            rstr += ' )'

        rstr += ' )'
        return rstr


    def parse_sentence(self, sentence):
        self.parse(sentence)
        print self.backward()



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


def main():
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  #addonoffarg(parser, 'input', help="parse mode", default=False)
  parser.add_argument("--train", "-t", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="train file (ignored)")
  parser.add_argument("--infile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input file (ignored)")
  parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file (grammar)")

  try:
    args = parser.parse_args()
    #print args
  except IOError as msg:
    parser.error(str(msg))

  workdir = tempfile.mkdtemp(prefix=os.path.basename(__file__), dir=os.getenv('TMPDIR', '/tmp'))
  trainfile = prepfile(args.train, 'r')
  infile = prepfile(args.infile, 'r')
  outfile = prepfile(args.outfile, 'w')

  gp = GrammarParser()
  #out = open(args["--infile"], 'w')
  out = outfile
  sys.stdout = out
  for line in infile:
  #open(args["--outfile"]):
      b = gp.viterbi_parse(line)
      # print b
      if b == 'Not Parse Successful':
          # line.strip('\n') + '\t' +
          # out.write(line)
          out.write('\n')
      else:
          gp.print_tree('TOP', 0, gp.word_num, gp.backpointer)
          # out.write('\n')
          # sys.stdout.write(str(b )+ '\n')
          sys.stdout.write('\n')
          # print
  out.close()

  def cleanwork():
    shutil.rmtree(workdir, ignore_errors=True)

if __name__ == "__main__":
    main()


