import readYelp
import words
import businessVectors

def getWords(i=0):
    (l, d) = readYelp.readY('../yelp/yelp_academic_dataset_review.json', i)
    #(l, d) = readYelp.readY('../../hw1/yelp/yelp_academic_dataset_review.json', 50000)
    print "Got the data! Got ", l, " lines of data"
    (all_w, per) = words.bagOfWords(d)
    return (all_w, per)

def getBussVector(i=0):
    (l, d) = readYelp.readY('../yelp/yelp_academic_dataset_business.json', i)
    #(l, d) = readYelp.readY('../../hw1/yelp/yelp_academic_dataset_review.json', 50000)
    print "Got the data! Got ", l, " lines of data"
    (n, vectors) = businessVectors.bussFeatureVector(d)
    return (n, vectors)


#n,d = getBussVector(100)
