from __future__ import division
from tree import Tree

class LearnGrammar:
    count_dict = {}
    start_dict = {}
    terminal_dict = {}

    def __init__(self):
        finput_tree = open("train.trees.pre.unk", mode='r')
        #finput_tree = training_name
        while 1:
            line = finput_tree.readline()
            #print line
            if not line:
                break
            #line = line.replace('*', '')
            t = Tree.from_str(line)
            #print t
            self.traverse_tree(t.root)
        finput_tree.close()

    def traverse_tree(self, root):
        root_str = root.label
        child_str = ''

        for each in root.children:
            child_str += ' '
            child_str += each.label
            # recursive
            self.traverse_tree(each)


        if len(root.children) == 0:
            return

        if len(root.children) == 1:
            if root.children[0].label.lower() not in self.terminal_dict:
                self.terminal_dict[root.children[0].label.lower()] = set()
            self.terminal_dict[root.children[0].label.lower()].add(root.label)

            one_child_str = root.children[0].label.lower()
            if root_str + ' ' + one_child_str in self.count_dict:
                self.count_dict[root_str + ' ' + one_child_str] += 1
            else:
                self.count_dict[root_str + ' ' + one_child_str] = 1

            if root_str in self.start_dict:
                self.start_dict[root_str].add(root_str + ' ' + one_child_str)
            else:
                self.start_dict[root_str] = set()
                self.start_dict[root_str].add(root_str + ' ' + one_child_str)
        else:
            if root_str + child_str in self.count_dict:
                self.count_dict[root_str + child_str] += 1
            else:
                self.count_dict[root_str + child_str] = 1

            if root_str in self.start_dict:
                self.start_dict[root_str].add(root_str + child_str)
            else:
                self.start_dict[root_str] = set()
                self.start_dict[root_str].add(root_str + child_str)

    def write_PCFG_grammar(self):
        foutput = open('pcfggrammar.txt', 'w')

        for k, v in self.start_dict.iteritems():
            sum = 0
            for i in v:
                sum += self.count_dict[i]
            for i in v:
                self.count_dict[i] = ("%.10f" % (self.count_dict[i] / sum))
                word_list = i.split()
                output_str = word_list[0] + ' -> '
                for index in range(1, len(word_list)):
                    output_str += ' '
                    output_str += word_list[index]
                output_str = output_str + ' # ' + str(self.count_dict[i]) + '\n'
                foutput.writelines(output_str)
                foutput.writelines("")
        foutput.close()


if __name__ == "__main__":
    lg = LearnGrammar()
    max_num = 0
    rule = ''
    for each in lg.count_dict:
        if lg.count_dict[each] > max_num:
            max_num = lg.count_dict[each]
            rule = each
    print 'The total number of rule: ' + str(len(lg.count_dict))
    print 'Most Frequent Rule: ' + rule
    print 'The number of the most frequent rule: ' + str(max_num)
    #print lg.start_dict
    #print lg.count_dict
    #print lg.terminal_dict
    lg.write_PCFG_grammar()


