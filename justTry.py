import readYelp
import words
import businessVectors
import businessFeatureVector as bfv
import userReview

def getWords(i=0):
    (l, d) = readYelp.readY('../yelp/yelp_academic_dataset_review.json', i)
    print "Got the data! Got ", l, " lines of data"
    (all_w, per) = words.bagOfWords(d)
    return (all_w, per)

def getBusVector(i=0):
    (l, d) = readYelp.readY('../yelp/yelp_academic_dataset_business.json', i)
    print "Got the data! Got ", l, " lines of data"
    (n, vectors) = businessVectors.busFeatureVector(d)
    return (n, vectors)

def getBusFeatVector(i=0):
    (l, d) = readYelp.readY('../yelp/yelp_academic_dataset_business.json', i)
    print "Got the data! Got ", l, " lines of data"
    featVectors = [bfv.Business(bus) for bus in d]
    #(n, vectors) = businessVectors.busFeatureVector(d)
    return featVectors

def getUserReviews(i=0):
    (l, d) = readYelp.readY('../yelp/yelp_academic_dataset_review.json', i)
    print "Got the data! Got ", l, " lines of data"
    per = userReview.reviewsPerUser(d)
    return per
    n
def crossUserReviewsBus(minrev=15, maxrev=1000,  i=0):
    d_user = getUserReviews(i)
    (n, d_buss) = getBusVector(i)
    output = {}
    for user, revs in d_user.iteritems():
        to_delete = []
        for buss in revs:
            if not buss in d_buss:
                to_delete.append(buss)
        for buss in to_delete:
            del d_user[user][buss]
        if len(d_user[user])>=minrev and  len(d_user[user])<=maxrev:
            output[user] = d_user[user]
    return (output, d_buss)


#n,d = getBusVector(100)
#d = getUserReviews(10)


 
