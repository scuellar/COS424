import justTry

from numpy import array
from scipy.sparse import lil_matrix
from scipy.io import mmwrite

def getMatrix(filename, n=0, nump = True):

    reviews = justTry.getUserReviews(n)
	
    user_IDs = reviews.keys()
    nUsers = len(user_IDs)
	
    bus = justTry.getBusVector(n)
    bus = bus[1]
    bus_IDs = bus.keys()
    nBus = len(bus_IDs)
	# turn bus' value into column ids
    for i, bid in enumerate(bus_IDs):
        bus[bid] = i

	# full array is very large, outputting as Matrix Market format later on
    rmatrix = lil_matrix((nUsers,nBus))

	# for each userID (row), find all ratings and place them in the appropriate location in rmatrix
    for row, uid in enumerate(user_IDs):
        revs = reviews[uid]						# reviews this user made (dic)
        rev_IDs = reviews[uid].keys()			# ids of businesses this user has reviewed
        for bid in rev_IDs:	
            if bid in bus:						# some businesses not in our list				
                col = bus[bid] 						# column associated with business
                rmatrix[row,col] = revs[bid]
                
    mmwrite(filename, rmatrix) 		# 70817 x 3654
    return rmatrix


#getMatrix("factorization_trials/fact_ratings_matrix.txt")

