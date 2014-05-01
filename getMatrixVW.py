import justTry
import string

# auxiliary function for the predictions file, if necessary
# ATTENTION: procudes 5GB+ text file
def makeVWLine(filename, row, nCols):
	fin = open(filename, 'w')
	for row in range(0, nUsers):
		fin.write("\n".join(' |u '+str(row)+' |i '+str(i)+'\n' for i in range(0, nCols)))
		if (row%5000) == 0:
			print 'Wrote '+str(row)+' lines.'
	fin.close()

# Generates two files:
#   filename - sparse representation of ratings matris in Vowpal-Wabbit format
#   filename_input.txt - predictions text file 
def getMatrixVW(filename):
    
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


	f = open(filename, 'w')
	# for each userID (row), write ratings to file
	for row, uid in enumerate(user_IDs):
		revs = reviews[uid]						# reviews this user made (dic)
		rev_IDs = reviews[uid].keys()			# ids of businesses this user has reviewed
		for bid in rev_IDs:	
			if bid in bus:						# some businesses not in our list				
				col = bus[bid] 						# column associated with business
				f.write(str(revs[bid])+' |u '+str(row)+' |i '+str(col)+'\n')

	f.close()

	# uncomment to output predictions file as well
	# fname = string.split(filename,'.')
	# fname = fname[0]+'_input.txt'
	# makeVWLine(fname)


getMatrixVW("ratingsVW.txt")

