import justTry
from sklearn.linear_model import LinearRegression, Lasso, Ridge
import numpy as np
import math
from copy import deepcopy

bus = justTry.getBusFeatVector()
userrevs = justTry.getUserReviews()

for business in bus:
    business.dico["reviews"] = {}

bustab = {business.id:business for business in bus}

trainuserrevs = {}
testuserrevs = {}
count = 0
for user in userrevs.keys():
    for review in userrevs[user]:
        if count % 10 == 0:
            if testuserrevs.get(user, None) is None:
                testuserrevs[user] = {}
            testuserrevs[user][review] = userrevs[user][review]
        else:
            if trainuserrevs.get(user, None) is None:
                trainuserrevs[user] = {}
            trainuserrevs[user][review] = userrevs[user][review]
        count += 1
        

for user in trainuserrevs.keys():
    for business in trainuserrevs[user].keys():
        bustab[business].dico["reviews"][user] = trainuserrevs[user][business]

total = 0
count = 0
for user in trainuserrevs.keys():
    for business in trainuserrevs[user].keys():
        total += trainuserrevs[user][business]
        count += 1

revavg = total/float(count)

def specialAvg(items, key):
    nums = [items[item] for item in items.keys() if item != key]
    if len(nums) > 0:
        return sum(nums)/float(len(nums))
    else:
        return revavg

trainvec = []
for key in trainuserrevs.keys():
    trainvecinternal = []
    for business in trainuserrevs[key].keys():
        busvec = bustab[business].vector
        busvec[69] = specialAvg(bustab[business].dico["reviews"],key)
        np.append(busvec, specialAvg(trainuserrevs[key], business))
        trainvecinternal.append((key, business, trainuserrevs[key][business], busvec))
    trainvec.append(trainvecinternal)


#trainvec = [[(key, business, trainuserrevs[key][business], np.append(bustab[business].vector,specialAvg(bustab[business],key))) for business in trainuserrevs[key].keys()] for key in trainuserrevs.keys()]

testvec = []
for key in testuserrevs.keys():
    testvecinternal = []
    for business in testuserrevs[key].keys():
        busvec = bustab[business].vector
        busvec[69] = specialAvg(bustab[business].dico["reviews"],key)
        np.append(busvec, specialAvg(testuserrevs[key], business))
        testvecinternal.append((key, business, testuserrevs[key][business], busvec))
    testvec.append(testvecinternal)


#testvec = [[(key, business, testuserrevs[key][business], np.append(bustab[business].vector,revavg)) for business in testuserrevs[key].keys()] for key in testuserrevs.keys()]

actualtrainvec = []
map(actualtrainvec.extend, trainvec)

trainuserids = []
trainbusinessids = []
trainactualratings = []
trainvectors = []
for (user, business, actualrating, vec) in actualtrainvec:
    trainuserids.append(user)
    trainbusinessids.append(business)
    trainactualratings.append(actualrating)
    trainvectors.append(vec)

actualtestvec = []
map(actualtestvec.extend, testvec)

testuserids = []
testbusinessids = []
testactualratings = []
testvectors = []
for (user, business, actualrating, vec) in actualtestvec:
    testuserids.append(user)
    testbusinessids.append(business)
    testactualratings.append(actualrating)
    testvectors.append(vec)

xtrain = trainvectors
xtest = testvectors
ytrain = trainactualratings
ytest = testactualratings

lreg = LinearRegression()
lreg.fit(xtrain, ytrain, n_jobs=-1)

lasso = Lasso()
lasso.fit(xtrain, ytrain)

ridge = Ridge()
ridge.fit(xtrain, ytrain)

lregpredictions = lreg.predict(xtest)
lassopredictions = lasso.predict(xtest)
ridgepredictions = ridge.predict(xtest)

sqerrors = [(test - pred)**2 for test, pred in zip(ytest, lregpredictions)]
sqerror = sum(sqerrors)/float(len(sqerrors))

abserrors = [abs(test - pred) for test, pred in zip(ytest, lregpredictions)]
abserror = sum(abserrors)/float(len(abserrors))

print "Linear:", math.sqrt(sqerror), abserror

sqerrors = [(test - pred)**2 for test, pred in zip(ytest, lassopredictions)]
sqerror = sum(sqerrors)/float(len(sqerrors))

abserrors = [abs(test - pred) for test, pred in zip(ytest, lassopredictions)]
abserror = sum(abserrors)/float(len(abserrors))

print "Lasso:", math.sqrt(sqerror), abserror

sqerrors = [(test - pred)**2 for test, pred in zip(ytest, ridgepredictions)]
sqerror = sum(sqerrors)/float(len(sqerrors))

abserrors = [abs(test - pred) for test, pred in zip(ytest, ridgepredictions)]
abserror = sum(abserrors)/float(len(abserrors))

print "Ridge:", math.sqrt(sqerror), abserror

