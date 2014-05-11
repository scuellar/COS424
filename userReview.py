"""Rturns a dictionary of dictionaries mapping user_ID -> user_ID -> stars """
from random import shuffle

def reviewsPerUser(dic, verb = False):
    revPerUser = {}    
    for n, review in enumerate(dic):
        user_ID = review.get("user_id", None)
        bus_ID = review.get("business_id", None)
        stars = review.get("stars", None)
        if (user_ID is None or bus_ID is None):
            print "Useless review here without User ID, Business ID or stars. Number", n
        prev = revPerUser.get(user_ID, {})
        prev[bus_ID] = stars
        revPerUser[user_ID] = prev
        
        if verb and n>0 and n%5000==0:
            print n," Reviews processed..."
    return revPerUser

def reviewsPerUserTest(dic, verb = False, n = 10):
    revPerUserTest = {} 
    revPerUserTrain = {} 
    leng = len(dic)
    print "Got ", leng, " reviews"
    orderer = [0]*leng
    for i in xrange(0, leng, n):
        orderer[i:i+n] = range(len(orderer[i:i+n]))
    shuffle(orderer)
    for n, review in enumerate(dic):
        user_ID = review.get("user_id", None)
        bus_ID = review.get("business_id", None)
        stars = review.get("stars", None)
        if (user_ID is None or bus_ID is None):
            print "Useless review here without User ID, Business ID or stars. Number", n
        if orderer[n]==0:
            per = revPerUserTest.get(user_ID, {})
            per[bus_ID] = stars
            revPerUserTest[user_ID] = per
        else:
            per = revPerUserTrain.get(user_ID, {})
            per[bus_ID] = stars
            revPerUserTrain[user_ID] = per
        
        if verb and n>0 and n%5000==0:
            print n," Reviews processed..."
    print "Train set size", len(revPerUserTrain)
    print "Train set size", len(revPerUserTest)
    return (revPerUserTrain, revPerUserTest)
