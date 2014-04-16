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
    
#output = dic{user_id -> dic{bus_id -> stars}}
#d_bus = dic{bus_id -> FV}
def crossUserReviewsBus(k=15, i=0):
    d_user = getUserReviews(i)
    d_bus = getBusVector(i)
    output = {}
    for user in d_user:
        for bus in d_user[user]:
            to_delete = []
            if not bus in d_bus:
                to_delete.append(bus)
        for buss in to_delete:
            del d_user[user][bus]
        if len(d_user[user])>=k:
            output[user] = d_user[user]
    return (output, d_bus)


#n,d = getBusVector(100)
#d = getUserReviews(10)


 
