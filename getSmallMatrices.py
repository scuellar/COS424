import justTry
import getMatrix
from numpy import array
from scipy.sparse import lil_matrix
from scipy.io import mmwrite

def getMatrices(reviews, filename = "", clusters = [], n=0, nump = True):
    if len(clusters) == 0:
        getMatrix.getMatrix(filename, n, nump)
        return ()
    else:
        leng = len(clusters)
        
        #reviews = justTry.getUserReviews(n)
	
    user_IDs = reviews.keys()
    nUsers = len(user_IDs)

    #Dico with bus to position
    busPosition = {}
    for clusterN, cluster in enumerate(clusters):
         for index, bus in enumerate(cluster):
             busPosition[bus] = (clusterN, index)
    
    # full array is very large, outputting as Matrix Market format later on
    rmatrices = [[] for _ in range(leng)]
    for i, cluster in enumerate(clusters):
        rmatrices[i] = lil_matrix((nUsers,len(cluster)))
    
	# for each userID (row), find all ratings and place them in the appropriate location in rmatrices
    userToPosition = {}
    userToPositionPerClus = {}
    for row, uid in enumerate(user_IDs):
        userToPosition[uid] = row
        revs = reviews[uid]						# reviews this user made (dic)
        rev_IDs = reviews[uid].keys()			# ids of businesses this user has reviewed
        for bid in rev_IDs:
            (clusterN, index) = busPosition[bid]
            perCluster = userToPositionPerClus.get(clusterN, {})
            perCluster[uid] = row
            userToPositionPerClus[clusterN] = perCluster
            rmatrices[clusterN][row,index] = revs[bid]
              
    #for i in range(leng):
        #mmwrite(str(i) + filename, rmatrices[i]) 		# 70817 x 3654
    return (rmatrices, busPosition, userToPosition, userToPositionPerClus)
