import readYelp
import words
import businessVectors

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


#n,d = getBussVector(100)
