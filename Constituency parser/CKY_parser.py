import math
from tree import Tree
import sys
import time

rules = {}  # maps from left of rule to right of rule to frequency
prob = {}  # maps from left of rule to right of rule to conditional probability
terminals = {}  # maps from terminal (right) to left of rule


def read_trees():
    for line in open("train.trees.pre.unk"):
        t = Tree.from_str(line)
        for node in t.bottomup():
            if node.children == []:
                continue
            counter = 0
            right = ''
            for child in node.children:
                counter += 1
                if len(node.children) == 1:  # check syntax
                    if child.label.lower() not in terminals:
                        terminals[child.label.lower()] = set()
                    terminals[child.label.lower()].add(node.label)
                if counter == 1:
                    right = right + child.label
                else:
                    right = right + ' ' + child.label
            if node.label not in rules:
                rules[node.label] = {}
            if right in rules[node.label]:
                if right not in terminals:
                    rules[node.label][right] += 1
                else:
                    rules[node.label][right.lower()] += 1
            else:
                if right.lower() not in terminals:
                    rules[node.label][right] = 1
                else:
                    rules[node.label][right.lower()] = 1


def count_rules():
    unique_rules = 0
    for rule in rules:
        for right in rules[rule]:
            unique_rules += 1


def cond_prob():
    left_count = 0
    for rule in rules:
        prob[rule] = {}
        for right in rules[rule]:
            left_count += rules[rule][right]
        for right in rules[rule]:
            prob[rule][right] = float(rules[rule][right]) / left_count
        left_count = 0


def viterbi_cky(string):
    before = time.time()
    s = string.split()

    best = {}  # dictionary of dictionary of dictionaries
    back = {}  # back pointers

    # initialize everything to 0
    for i in range(0, len(s) + 1):
        best[i] = {}
        back[i] = {}
        for j in range(0, len(s) + 1):
            best[i][j] = {}
            back[i][j] = {}
            for rule in rules:
                best[i][j][rule] = 0
                back[i][j][rule] = []

    # terminal probabilities
    for i in range(1, len(s) + 1):  # check end of range
        if s[i - 1].lower() in terminals:
            word = s[i - 1]
        else:
            word = '<unk>'
        for left in terminals[word.lower()]:
            if prob[left][word.lower()] > best[i - 1][i][left]:
                best[i - 1][i][left] = prob[left][word.lower()]
                back[i - 1][i][left].append(word)

    # update probabilities
    for l in range(2, len(s) + 1):  # check end of range
        for i in range(0, len(s) + 1 - l):  # check end of range
            j = i + l
            for k in range(i + 1, j):  # check end of range
                for rule in rules:
                    for right in rules[rule]:
                        r = right.split()
                        if len(r) == 1:
                            continue
                        else:
                            p = prob[rule][right] * best[i][k][r[0]] * best[k][j][r[1]]
                            if p > best[i][j][rule]:
                                best[i][j][rule] = p
                                back[i][j][rule] = []
                                back[i][j][rule].append(r[0])
                                back[i][j][rule].append(r[1])
                                back[i][j][rule].append(k)
    after = time.time()
    print str(math.log(len(s))) + ',' + str(math.log(after - before))
    if not back[0][len(s)]['TOP']:
        sys.stdout.write('')
    else:
        print_tree('TOP', 0, len(s), back)
    #if not best[0][len(s)]['TOP']:
    #    return 'None'
    #else:
    #    return str(math.log(best[0][len(s)]['TOP'], 10))


def print_tree(rule, i, j, back):
    if len(back[i][j][rule]) == 1:
        sys.stdout.write('(' + rule + ' ' + back[i][j][rule][0] + ')')
    else:
        sys.stdout.write('(' + rule + ' ')
        print_tree(back[i][j][rule][0], i, back[i][j][rule][2], back)
        sys.stdout.write(' ')
        print_tree(back[i][j][rule][1], back[i][j][rule][2], j, back)
        sys.stdout.write(')')


if __name__ == '__main__':
    read_trees()
    count_rules()
    cond_prob()
    #sentence = 'The flight should be eleven a.m tomorrow .'
    sentence = 'What is M I A ?'
    print '%%%%%%%%%%%%%%%%%%%%%%5'
    print viterbi_cky(sentence)
    print len(rules)
    '''
    read_trees()
    count_rules()
    cond_prob()
    out = open('dev.strings.out', 'w')
    for line in open("dev.strings"):
        b = viterbi_cky(line)
        out.write(line.strip('\n') + '\t' + b + '\n')
        # print
    out.close()
    '''
