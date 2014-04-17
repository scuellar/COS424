from sklearn.linear_model import LinearRegression, Lasso, Ridge
import justTry
import displayRegression

def fitprederr(classifier, xtrain, ytrain, xtest, ytest):
    classifier.fit(xtrain, ytrain)
    
    predictions = classifier.predict(xtest)
    
    sqerrors = [(test - pred)**2 for test, pred in zip(ytest, predictions)]
    sqerror = sum(sqerrors)/float(len(sqerrors))
    
    abserrors = [abs(test - pred) for test, pred in zip(ytest, predictions)]
    abserror = sum(abserrors)/float(len(abserrors))
    
    return (sqerror, abserror)
    

users, businesses = justTry.crossUserReviewsBus(minrev=100,maxrev=10000)

linearsq = []
linearabs = []
lassosq = []
lassoabs = []
ridgesq = []
ridgeabs = []

frac1 = 9
frac2 = 10


for i, user in zip(range(0, len(users.keys())), users.keys()):
    ratedbusinesses = users[user]

    split = frac1*(len(ratedbusinesses.values())/frac2)
    
    y = ratedbusinesses.values()[:split]
    x = [businesses[bus_id] for bus_id in ratedbusinesses.keys()][:split]
    
    cvlinearsq = []
    cvlinearabs = []
    cvlassosq = []
    cvlassoabs = []
    cvridgesq = []
    cvridgeabs = []

    for j in range(0, frac1):
        xtrain = [x[k] for k in range(0, len(x)) if k%frac1!=j]
        xtest = [x[k] for k in range(0, len(x)) if k%frac1==j]
        
        ytrain = [y[k] for k in range(0, len(y)) if k%frac1!=j]
        ytest = [y[k] for k in range(0, len(y)) if k%frac1==j]

        lreg = LinearRegression()
        lasso = Lasso()
        ridge = Ridge()
    
        cvlinsqerror, cvlinabserror = fitprederr(lreg, xtrain, ytrain, xtest, ytest)
        cvlassqerror, cvlasabserror = fitprederr(lasso, xtrain, ytrain, xtest, ytest)
        cvridsqerror, cvridabserror = fitprederr(ridge, xtrain, ytrain, xtest, ytest)

        cvlinearsq.append(cvlinsqerror)
        cvlinearabs.append(cvlinabserror)
        cvlassosq.append(cvlassqerror)
        cvlassoabs.append(cvlasabserror)
        cvridgesq.append(cvridsqerror)
        cvridgeabs.append(cvridabserror)

    
    linsqerror = sum(cvlinearsq)/float(len(cvlinearsq))
    linabserror = sum(cvlinearabs)/float(len(cvlinearabs))
    lassqerror = sum(cvlassosq)/float(len(cvlassosq))
    lasabserror = sum(cvlassoabs)/float(len(cvlassoabs))
    ridsqerror = sum(cvridgesq)/float(len(cvridgesq))
    ridabserror = sum(cvridgeabs)/float(len(cvridgeabs))

    linearsq.append(linsqerror)
    linearabs.append(linabserror)
    lassosq.append(lassqerror)
    lassoabs.append(lasabserror)
    ridgesq.append(ridsqerror)
    ridgeabs.append(ridabserror)
    
linsqerror = sum(linearsq)/float(len(linearsq))
linabserror = sum(linearabs)/float(len(linearabs))
print "CV: Avg Linear:", linsqerror, linabserror

lassqerror = sum(lassosq)/float(len(lassosq))
lasabserror = sum(lassoabs)/float(len(lassoabs))
print "CV: Avg Lasso:", lassqerror, lasabserror

ridsqerror = sum(ridgesq)/float(len(ridgesq))
ridabserror = sum(ridgeabs)/float(len(ridgeabs))
print "CV: Avg Ridge:", ridsqerror, ridabserror

displayRegression.displayRegression(linearsq, ridgesq, lassosq)
displayRegression.displayRegressionInOrder(linearsq, ridgesq, lassosq,users)

linearsq = []
linearabs = []
lassosq = []
lassoabs = []
ridgesq = []
ridgeabs = []
dumbsq = []
dumbabs = []

for i, user in zip(range(0, len(users.keys())), users.keys()):
    ratedbusinesses = users[user]
    
    y = ratedbusinesses.values()
    x = [businesses[bus_id] for bus_id in ratedbusinesses.keys()]


    split = frac1*(len(x)/frac2)
    
    xtrain = x[:split]
    xtest = x[split:]
    
    ytrain = y[:split]
    ytest = y[split:]

    lreg = LinearRegression()
    lasso = Lasso()
    ridge = Ridge()
    
    linsqerror, linabserror = fitprederr(lreg, xtrain, ytrain, xtest, ytest)
    linearsq.append(linsqerror)
    linearabs.append(linabserror)

    lassqerror, lasabserror = fitprederr(lasso, xtrain, ytrain, xtest, ytest)
    lassosq.append(lassqerror)
    lassoabs.append(lasabserror)

    ridsqerror, ridabserror = fitprederr(ridge, xtrain, ytrain, xtest, ytest)
    ridgesq.append(ridsqerror)
    ridgeabs.append(ridabserror)

    dumbpred = [features[0] for features in x]

    dumbsqerrors = [(test - pred)**2 for test, pred in zip(ytest, dumbpred)]
    dumbsqerror = sum(dumbsqerrors)/float(len(dumbsqerrors))
    
    dumbabserrors = [abs(test - pred) for test, pred in zip(ytest, dumbpred)]
    dumbabserror = sum(dumbabserrors)/float(len(dumbabserrors))

    dumbsq.append(dumbsqerror)
    dumbabs.append(dumbabserror)

linsqerror = sum(linearsq)/float(len(linearsq))
linabserror = sum(linearabs)/float(len(linearabs))
print "Test: Avg Linear:", linsqerror, linabserror

lassqerror = sum(lassosq)/float(len(lassosq))
lasabserror = sum(lassoabs)/float(len(lassoabs))
print "Test: Avg Lasso:", lassqerror, lasabserror

ridsqerror = sum(ridgesq)/float(len(ridgesq))
ridabserror = sum(ridgeabs)/float(len(ridgeabs))
print "Test: Avg Ridge:", ridsqerror, ridabserror

dumbsqerror = sum(dumbsq)/float(len(dumbsq))
dumbabserror = sum(dumbabs)/float(len(dumbabs))
print "Test: Avg Dumb:", dumbsqerror, dumbabserror

displayRegression.displayRegressionCompare1(ridgesq, dumbsq)
displayRegression.displayRegressionCompare(ridgesq, dumbsq, users)

