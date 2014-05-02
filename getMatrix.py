#!/usr/bin/python

import justTry
import random, pickle
from numpy import array
from scipy.sparse import lil_matrix
from scipy.io import mmwrite


# acquires business vectors
# constructs a map between business IDs and integers
def getBusinesses():
	bus = justTry.getBusVector() 				
	bus = bus[1] 								# bus = dictionary: key-bID; val-feature vector
	bus_IDs = bus.keys() 						# distinct business ids
	nBus = len(bus_IDs) 						# number of distinct businesses
	busVals = {} 								
	for i, bid in enumerate(sorted(bus_IDs)):
		busVals[bid] = i
	return nBus, bus, busVals



# acquires reviews
# unpacks reviews into flat list [(userID, busID, rating)]
# constructs a map between user IDs and integers
def getReviewList(bus):
	reviews = justTry.getUserReviews() 		
	user_IDs = reviews.keys() 					# distinct user ids
	nUsers = len(user_IDs) 						# number of distinct users
	reviewList = []
	for i, uid in enumerate(user_IDs):
		revs = reviews[uid]
		rev_IDs = reviews[uid].keys()
		for bid in rev_IDs:
			if bid in bus:
				reviewList += [(uid, bid, revs[bid])]
	nReviews = len(reviewList)
	userVals = {}
	for i, uid in enumerate(sorted(user_IDs)):
		userVals[uid] = i
	return nUsers, reviewList, userVals



# see doc_string
def getMatrix(prefix, n=1, groups=None):
	""" prefix -- prefix to filenames
		n 	   -- number of groups (if user wants equal sized groups)
		groups -- 'stochastic list/tuple' (i.e. sums to 1, and entries in [0,1])

		getMatrix produces one file for each group, where the number of entries
		in each group is defined by the corresponding tuple entry (0.1=10pc of all reviews)

		getMatrix produces two extra files:
			<prefix>_users.csv
			<prefix>_businesses.csv
			each line is of the form 'num, id' - used to associate row/col numbers to ids
		"""
	
	nBus, bus, busVals = getBusinesses()

	nUsers, reviews, userVals = getReviewList(bus)
	nReviews = len(reviews)

	# add randomness (randomly shuffle list in place)
	random.seed('group4')
	random.shuffle(reviews)

	if (groups != None):
		groups = [int(nReviews*groups[i]) for i in range(0, len(groups))]
		groups[len(groups)-1] += nReviews-sum(groups) 		# adds leftovers to last group
	else:
		groups = [int(nReviews/n)]*n
		groups[len(groups)-1] += nReviews-sum(groups)

	
	low = 0
	# build matrix for each group
	for i in range(0, len(groups)):
		print 'Writing matrix: '+str(i)+'...'
		rmatrix = lil_matrix((nUsers, nBus))
		# iterate through all reviews on this group
		for rev in reviews[low:low+groups[i]]:
			uid, bid, rating = rev
			rmatrix[userVals[uid], busVals[bid]] = rating
		low += groups[i]
		# write this groups matrix
		mmwrite(prefix+str(i)+'.mtx', rmatrix)


	# dump text files
	print 'Writing users text file...'
	f = open(prefix+'_users.csv', 'w')
	for uid, num in sorted(userVals.iteritems()):
		f.write(str(num)+','+uid+'\n')
	f.close()
	print 'Writing businesses text file...'
	f = open(prefix+'_businesses.csv', 'w')
	for bid, num in sorted(busVals.iteritems()):
		f.write(str(num)+','+bid+'\n')
	f.close()



if __name__=="__main__":
	getMatrix('ratingsTT', groups=(0.9, 0.1))