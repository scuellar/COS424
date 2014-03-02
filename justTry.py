import readYelp
import words

def getWords():
    (l, d) = readYelp.readY('../../hw1/yelp/yelp_academic_dataset_review.json', 50000)
    print "Got the data! Got ", l, " lines of data"
    (all_w, per) = words.bagOfWords(d)
    #print "All: ", all_w
    #print "Per review: ", per
    print l

    return all_w, per
