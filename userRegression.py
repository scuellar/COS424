from sklearn.linear_model import LinearRegression, Lasso, Ridge
import justTry
import displayRegression

users, businesses = justTry.crossUserReviewsBus(k=200)

linearsq = []
linearabs = []
lassosq = []
lassoabs = []
ridgesq = []
ridgeabs = []


for i, user in zip(range(0, len(users.keys())), users.keys()):
    ratedbusinesses = users[user]
    
    y = ratedbusinesses.values()
    x = [businesses[bus_id] for bus_id in ratedbusinesses.keys()]


    split=int(9*len(y))/10
    
    ytrain = y[:split]
    ytest = y[split:]
    
    xtrain = x[:split]
    xtest = x[split:]
    
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
    
    linearsq.append(sqerror)
    linearabs.append(abserror)
    print i, "Linear:", sqerror, abserror
    
    sqerrors = [(test - pred)**2 for test, pred in zip(ytest, lassopredictions)]
    sqerror = sum(sqerrors)/float(len(sqerrors))
    
    abserrors = [abs(test - pred) for test, pred in zip(ytest, lassopredictions)]
    abserror = sum(abserrors)/float(len(abserrors))
    
    lassosq.append(sqerror)
    lassoabs.append(abserror)
    print i, "Lasso:", sqerror, abserror
    
    sqerrors = [(test - pred)**2 for test, pred in zip(ytest, ridgepredictions)]
    sqerror = sum(sqerrors)/float(len(sqerrors))
    
    abserrors = [abs(test - pred) for test, pred in zip(ytest, ridgepredictions)]
    abserror = sum(abserrors)/float(len(abserrors))
    
    ridgesq.append(sqerror)
    ridgeabs.append(abserror)
    print i, "Ridge:", sqerror, abserror

sqerror = sum(linearsq)/float(len(linearsq))
abserror = sum(linearabs)/float(len(linearabs))
print "Avg Linear:", sqerror, abserror

sqerror = sum(lassosq)/float(len(lassosq))
abserror = sum(lassoabs)/float(len(lassoabs))
print "Avg Lasso:", sqerror, abserror

sqerror = sum(ridgesq)/float(len(ridgesq))
abserror = sum(ridgeabs)/float(len(ridgeabs))
print "Avg Ridge:", sqerror, abserror


displayRegression.displayRegression(linearsq, ridgesq, lassosq)
