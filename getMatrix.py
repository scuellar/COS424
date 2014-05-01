import justTry
from numpy import array
from scipy.sparse import lil_matrix
from scipy.io import mmwrite

def getMatrix():
    
	reviews = justTry.getUserReviews()
	
	user_IDs = reviews.keys()
	nUsers = len(user_IDs)
	
	bus = justTry.getBusVector()
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

	mmwrite("ratings_matrix.mtx", rmatrix) 		# 70817 x 3654


getMatrix()

