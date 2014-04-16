import readYelp
import words
import businessVectors
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

def getUserReviews(i=0):
    (l, d) = readYelp.readY('../yelp/yelp_academic_dataset_review.json', i)
    print "Got the data! Got ", l, " lines of data"
    per = userReview.reviewsPerUser(d)
    return per
    
def crossUserReviewsBus(i=0):
    BOUND = 10
    d_user = getUserReviews(i)
    d_buss = getBusVector(i)
    output = {}
    for user in d_user:
        for buss in d_user[user]:
            to_delete = []
            if not buss in d_buss:
                to_delete.append(buss)
        for buss in to_delete:
            del d_user[user][buss]
        if len(d_user[user])>=15:
            output[user] = d_user[user]
    return output


#n,d = getBusVector(100)
#d = getUserReviews(10)


 
