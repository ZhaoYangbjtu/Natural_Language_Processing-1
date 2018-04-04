import numpy as np
from numpy import random


def run_viterbi(emission_scores, trans_scores, start_scores, end_scores):
    """Run the Viterbi algorithm.

    N - number of tokens (length of sentence)
    L - number of labels

    As an input, you are given:
    - Emission scores, as an NxL array
    - Transition scores (Yp -> Yc), as an LxL array
    - Start transition scores (S -> Y), as an Lx1 array
    - End transition scores (Y -> E), as an Lx1 array

    You have to return a tuple (s,y), where:
    - s is the score of the best sequence
    - y is a size N array of integers representing the best sequence.
    """
    L = start_scores.shape[0]
    assert end_scores.shape[0] == L
    assert trans_scores.shape[0] == L
    assert trans_scores.shape[1] == L
    assert emission_scores.shape[1] == L
    N = emission_scores.shape[0]

    viterbi_score = [[0 for i in range(L)] for j in range(N)]
    path = [[0 for i in range(L)] for j in range(N)]

    maxScore = -1
    sequence = []
    current_score = -1
    current_path = -1

    for i in range(L):
        viterbi_score[0][i] = start_scores[i] + emission_scores[0][i]
        path[0][i] = i
        '''
        if viterbi_score[0][i] > current_score:
            current_score = viterbi_score[0][i]
            current_path = i
        '''

    #pre_path = current_path
    #pre_score = current_score
    #sequence.append(current_path)

    for i in range(1, N):
        current_score = -1
        current_path = -1
        for j in range(L): # current move
            max_path = -1
            max_score = -1000
            for m in range(L): # previous move
                # current we i - > j with previous from 0 - L
                current_score = viterbi_score[i - 1][m] + trans_scores[m][j] + emission_scores[i][j]
                #viterbi_score[i][j] = viterbi_score[i - 1][pre_path] * trans_scores[pre_path][j] * emission_scores[i][j]
                if current_score > max_score:
                    max_score = current_score
                    max_path = m

            viterbi_score[i][j] = max_score
            path[i][j] = max_path
        #sequence.append(current_path)


    max_score = -1000
    max_path = -1
    for i in range(L):
        if max_score < viterbi_score[N - 1][i] + end_scores[i]:
            max_score = viterbi_score[N - 1][i] + end_scores[i]
            max_path = i
            #print "YEs"
    #print max_path
    sequence.append(max_path)
    for i in range(N - 1, 0, -1):
        max_path = path[i][max_path]
        #print max_path
        sequence.append(max_path)
        #print sequence

    #print viterbi_score
    #print path
    sequence.reverse()
    ll = [max_score, sequence]
    return tuple(ll)

if __name__ == "__main__":

    maxN = 7  # maximum length of a sentence (min is 1)
    maxL = 4  # maximum number of labels (min is 2)

    emission_var = 1.0  # variance of the gaussian generating emission scores
    trans_var = 1.0  # variance of the gaussian generating transition scores

    N = random.randint(1, maxN + 1)
    L = random.randint(2, maxL + 1)


    # Generate the scores
    emission_scores = np.array([[0.11849646,  0.11396779,  0.37025538],
                       [1.04053075, -1.51698273, - 0.86627621],
                       [-0.05503512, -0.10731045,  1.36546718],
                       [-0.09769572, -2.42595457, - 0.4530558],
                       [-0.470771, 0.973016, -1.27814912]])

    trans_scores = np.array([[1.43737068, -0.07770457,  1.08963016],
                    [0.09654267,  1.41866711,  1.16827314],
                    [0.94718595, 1.08548703, 2.38222445]])

    start_scores = np.array([-0.40602374, 0.26644534, -1.35571372])

    end_scores = np.array([-0.11410253, -0.84423086,  0.70564081])
    # [0, 0, 2, 2, 2]


    print run_viterbi(emission_scores, trans_scores, start_scores, end_scores)

