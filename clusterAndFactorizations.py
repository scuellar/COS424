"""Quick file where I cluster the business and factorize with the resulting matrices"""
print "Importing modules..."
import getSmallMatrices as getSM
import clusterBusiness as clustBus
from factorization_trials import factorize_bias as fact_bias    
import numpy as np
from scipy import io
import scipy as sp
import justTry

"""Here I set the parameters!"""
clusters_k = 30 #Number of clusters
test_train = 5 # 1 + |Train|/|Test|
features = 10 #30 #Factorizing features (k)
lamb = 0.2 #factorizing lambda
lrate = .02 #Lrate
maxiters = 50

print "Clustering business.."
clustersBus = clustBus.clusterBusiness(k = clusters_k)
clusters = [[busn.id for busn in cluster] for cluster in clustersBus]

print "Getting the reviews..."
(train, test) = justTry.getReviewsTest(n = test_train)
print "Training set size: ", len(train)
print "Testing set size: ", len(test)

print "Making matrices out of clusters..."
(MS, busToPosition, userToPosition, userToPositionPerClus) = getSM.getMatrices(train, "fact_ratings_matrix.txt", clusters)


leng = len(MS)

def newList(n=5):
    return [0 for _ in range(n)]
(W,H,mymu,bu,bb) = (newList(leng),newList(leng),newList(leng),newList(leng),newList(leng))


print "factorizing matrices..."
for i, matrix in enumerate(MS):
    #np.seterr(all='print')
    #M = sp.io.mmread("fact_ratings_matrix.mtx")
    N = matrix.todok()
    (W[i],H[i],mymu[i],bu[i],bb[i]) = fact_bias.factorize_bias(N,features,lamb,lrate,maxiters)
    print "End of factorization: ", (i+1)

print "Building prediction matrices..."
predictionMatrices = [mymu[i] + bu[i] + bb[i] + np.dot(W[i], H[i]) for i in range(leng)]

print "computiung error..."
total_tests = [0] * leng
total_error = [0] * leng
total_serror = [0] * leng
unmatched_users = 0
for (user, reviews) in test.iteritems():
    #row = userToPosition.get(user, None)
    for (bus, stars) in reviews.iteritems():
        (clusterN, index) = busToPosition[bus]
        row = userToPositionPerClus.get(clusterN, {}).get(user, None)
        if row is None:
            #print "User ", user, " is not well defined... maybe he has no reviews? IDK..."
            unmatched_users += 1
        else:
            total_tests[clusterN] += 1
            prediction = predictionMatrices[clusterN][row , index]
            error = np.absolute(stars - prediction)
            total_error[clusterN] += error
            serror = (stars - prediction)**2
            total_serror[clusterN] += serror

print "Total of ", unmatched_users, " reviews were unpredictable..."
print "Total error: ", sum(total_error)
print "Average error per cluster: ", [(total_error[i]/float(total_tests[i])) for i in range(leng)]
print "Average error", (sum(total_error)/float(sum(total_tests)))
print "Average serror per cluster: ", [(total_serror[i]/float(total_tests[i])) for i in range(leng)]
print "Average serror", (sum(total_serror)/float(sum(total_tests)))
print "Average rmse per cluster: ", [(total_serror[i]/float(total_tests[i])) for i in range(leng)]
print "RMSE: ", np.sqrt(sum(total_serror)/float(sum(total_tests)))
print "Parameters:"
print "Clusters: ", clusters_k , ", train/train: ", test_train-1, ", k: ", features, ", lambda: ", lamb, ", lrate: ", lrate, ", iterations: ", maxiters

    
print "Done. Thank you for playing."
