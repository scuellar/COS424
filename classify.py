import numpy as np
from nltk.probability import FreqDist
from nltk.classify import SklearnClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

#pipeline = Pipeline([('tfidf', TfidfTransformer()),
#                     ('chi2', SelectKBest(chi2, k=1000)),
#                     ('nb', MultinomialNB())])
#classif = SklearnClassifier(pipeline)
classif = SklearnClassifier(MultinomialNB())

add_label = lambda lst, lab: [(x, lab) for x in lst]

import justTry

all_w, per = justTry.getWords(0)

print len(per[0]), len(per[1]), len(per[2]), len(per[3]), len(per[4]), 

train1 = (9*len(per[0]))/10
train2 = (9*len(per[1]))/10
train3 = (9*len(per[2]))/10
train4 = (9*len(per[3]))/10
train5 = (9*len(per[4]))/10

ones = [FreqDist(x) for x in per[0]]
twos = [FreqDist(x) for x in per[1]]
threes = [FreqDist(x) for x in per[2]]
fours = [FreqDist(x) for x in per[3]]
fives = [FreqDist(x) for x in per[4]]

print "Starting to train"
classif.train(add_label(ones[:train1], '1') + add_label(twos[:train2], '2') + add_label(threes[:train3], '3') + add_label(fours[:train4], '4') + add_label(fives[:train5], '5')) 
print "Done learning"
l_ones = np.array(classif.batch_classify(ones[train1:]))
print "one done"
l_twos = np.array(classif.batch_classify(twos[train2:]))
print "two done"
l_threes = np.array(classif.batch_classify(threes[train3:]))
print "three done"
l_fours = np.array(classif.batch_classify(fours[train4:]))
print "four done"
l_fives = np.array(classif.batch_classify(fives[train5:]))
print "five done"

con_ma = [[(l_ones == '1').sum(), (l_ones == '2').sum(), (l_ones == '3').sum(), (l_ones == '4').sum(), (l_ones == '5').sum()],
          [(l_twos == '1').sum(), (l_twos == '2').sum(), (l_twos == '3').sum(), (l_twos == '4').sum(), (l_twos == '5').sum()],
          [(l_threes == '1').sum(), (l_threes == '2').sum(), (l_threes == '3').sum(), (l_threes == '4').sum(), (l_threes == '5').sum()],
          [(l_fours == '1').sum(), (l_fours == '2').sum(), (l_fours == '3').sum(), (l_fours == '4').sum(), (l_fours == '5').sum()],
          [(l_fives == '1').sum(), (l_fives == '2').sum(), (l_fives == '3').sum(), (l_fives == '4').sum(), (l_fives == '5').sum()]]

print "Confusion matrix:\n%d\t%d\t%d\t%d\t%d\n%d\t%d\t%d\t%d\t%d\n%d\t%d\t%d\t%d\t%d\n%d\t%d\t%d\t%d\t%d\n%d\t%d\t%d\t%d\t%d\n" % (
          con_ma[0][0],con_ma[0][1],con_ma[0][2],con_ma[0][3],con_ma[0][4],
          con_ma[1][0],con_ma[1][1],con_ma[1][2],con_ma[1][3],con_ma[1][4],
          con_ma[2][0],con_ma[2][1],con_ma[2][2],con_ma[2][3],con_ma[2][4],
          con_ma[3][0],con_ma[3][1],con_ma[3][2],con_ma[3][3],con_ma[3][4],
          con_ma[4][0],con_ma[4][1],con_ma[4][2],con_ma[4][3],con_ma[4][4])

print " "
good = con_ma[0][0]+con_ma[1][1]+con_ma[2][2]+con_ma[3][3]+con_ma[4][4]
partial = [sum(l) for l in con_ma]
total = sum(partial)
print "Accuracy: ", float(good)/total
print " "
print con_ma


