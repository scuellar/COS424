import justTry
from sklearn.cluster import KMeans

def clusterBusiness(busNumber = 0, k = 8, max_iter=300, include_cats = True):
    # Get the business
    bfvs = justTry.getBusFeatVector(busNumber, include_cats = include_cats)

    # Make business matrix
    matrix = [bus.vector for bus in bfvs]

    # Get Names
    names = [bus.name for bus in bfvs]
    
    # 
    clusterer =  KMeans(k, max_iter=max_iter)
    clusterList = clusterer.fit_predict(bfvs)
    
    clusters = [[] for i in range(k)]
    for (cluster, business) in zip(clusterList, bfvs):
        clusters[cluster].append(business)
    
    return clusters


cb = clusterBusiness(k = 50)

import pickle
def write(data, outfile):
    f = open(outfile, "w+b")
    pickle.dump(data, f)
    f.close()

def printTo(data, outfile):
    f = open(outfile, "w+b")
    f.write(str(data))
    f.close()

printTo([[bus.name for bus in cluster] for cluster in cb], "clusterNames.txt")
write([[bus.id for bus in cluster] for cluster in cb], "clusterIds.txt")
