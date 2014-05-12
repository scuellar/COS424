import justTry
from sklearn.linear_model import LinearRegression, Lasso, Ridge
import numpy as np
import math

bus = justTry.getBusFeatVector()
userrevs = justTry.getUserReviews()

bustab = {business.id:business for business in bus}


ourvec = [[(key, business, userrevs[key][business], np.append(bustab[business].vector,sum(userrevs[key].values())/float(len(userrevs[key])))) for business in userrevs[key].keys()] for key in userrevs.keys()]

actualvec = []
map(actualvec.extend, ourvec)

userids = []
businessids = []
actualratings = []
vectors = []
for (user, business, actualrating, vec) in actualvec:
    userids.append(user)
    businessids.append(business)
    actualratings.append(actualrating)
    vectors.append(vec)

split = 9*(len(actualratings)/10)
xtrain = vectors[:split]
xtest = vectors[split:]
ytrain = actualratings[:split]
ytest = actualratings[split:]

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
