import readYelp
import words

(l, d) = readYelp.readY('../yelp/yelp_academic_dataset_review.json', 10)
print "Got the data! Got ", l, " lines of data"
(all_w, per) = words.bagOfWords(d)
print "All: ", all_w
print "Per review: ", per
print l
