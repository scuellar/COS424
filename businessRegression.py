from sklearn.linear_model import LinearRegression, Lasso, Ridge
import justTry

n, d = justTry.getBusVector()

y = [y[0] for y in d.values()]
x = [x[1:] for x in d.values()]

split = 9*(len(x)/10)

xtrain = x[:split]
xtest = x[split:]

ytrain = y[:split]
ytest = y[split:]

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

print "Linear:", sqerror, abserror

sqerrors = [(test - pred)**2 for test, pred in zip(ytest, lassopredictions)]
sqerror = sum(sqerrors)/float(len(sqerrors))

abserrors = [abs(test - pred) for test, pred in zip(ytest, lassopredictions)]
abserror = sum(abserrors)/float(len(abserrors))

print "Lasso:", sqerror, abserror

sqerrors = [(test - pred)**2 for test, pred in zip(ytest, ridgepredictions)]
sqerror = sum(sqerrors)/float(len(sqerrors))

abserrors = [abs(test - pred) for test, pred in zip(ytest, ridgepredictions)]
abserror = sum(abserrors)/float(len(abserrors))

print "Ridge:", sqerror, abserror
