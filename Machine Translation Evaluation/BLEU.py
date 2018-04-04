from nltk.stem.wordnet import WordNetLemmatizer
from nltk import ngrams
import string
import math
from scipy.stats.mstats import gmean

def read_files(data_file, answer_file, X, y):

    with open(data_file, 'r') as a:
        input1 = a.readline()
        count = 0

        while len(input1) != 0:

            hhr = input1.split(' ||| ')
            h1 = hhr[0].strip()
            h2 = hhr[1].strip()
            ref = hhr[2].strip()
            #rose(h1, h2, ref, ans, X, y)

            input1 = a.readline()



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





    precision_average1 = float(sum(precision_list1)) / max(len(precision_list1), 1)
    #print sum(precision_list1)
    #print precision_average1
    precision_average2 = float(sum(precision_list2)) / max(len(precision_list2), 1)
    #print sum(precision_list2)
    #print precision_average2


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

    bleu_h1 = gmean(precision_list1)
    bleu_h2 = gmean(precision_list2)


if __name__ == "__main__":
    h1 = "Republican leaders justify its policy necessary to combat electoral fraud.".strip()
    h2 = "Republican leaders justify its policy of necessity in the fight against electoral fraud.".strip()
    ref =   "Republican leaders justified their policy by the need to combat electoral fraud.".strip()


    get_feature(h1, h2, ref)