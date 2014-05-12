"""Quick file where I cluster the business and factorize with the resulting matrices"""
print "Importing modules..."
import getSmallMatrices as getSM
import clusterBusiness as clustBus
from factorization_trials import factorize_bias as fact_bias    
import numpy as np
from scipy import io
import scipy as sp
import justTry
import pickle

"""Here I set the parameters!"""
clusters_k = 30 #Number of clusters
test_train = 10 # 1 + |Train|/|Test|
features = 10 #30 #Factorizing features (k)
lamb = 0.2 #factorizing lambda
lrate = .02 #Lrate
maxiters = 100
folder = "cluster_matrices"


# clustering("clusters")
def clustering(fileClusters = "clusters", clusters_k = clusters_k, folder = folder):
    print "Clustering businesses.."
    clustersBus = clustBus.clusterBusiness(k = clusters_k)
    clusters = [[busn.id for busn in cluster] for cluster in clustersBus]
    for i in range(len(clustersBus)):
        text_file = open("cluster" +str(i) + ".txt", "w")
        text_file.write(str(clustersBus[i]))
        text_file.close()
    pickle.dump( clustersBus, open( folder+"/"+fileClusters + "_fullBus_" +".p", "wb" ) )
    pickle.dump( clusters, open( folder+"/"+fileClusters+".p", "wb" ) )
    print "Clusters writen in file: ", (fileClusters+".p")
    return clustersBus
#cl = clustering()

#reviewTrainTest("trainData","testData")
def reviewTrainTest(fileTrain = "trainData", fileTest = "testData", test_train = test_train, folder = folder):
    print "Getting the reviews..."
    (train, test) = justTry.getReviewsTest(n = test_train)

    pickle.dump( train, open( folder+"/"+fileTrain+".p", "wb" ) )
    pickle.dump( test,  open( folder+"/"+fileTest +".p", "wb" ) )
    print "Training and testing data saved in: ", (fileTrain+".p"), " and ", (fileTest +".p")
    return None
#reviewTrainTest()

#clusterMatrices("trainData", "postions", "clusters", folder)
def clusterMatrices(fileTrain = "trainData", filePositions = "postions", fileClusters = "clusters", fileMatrices = "cluster_matrix_", folder = folder):
    print "Making matrices out of clusters..."
    train = pickle.load( open( folder+"/"+fileTrain + ".p", "rb" ) )
    clusters = pickle.load( open( folder+"/"+fileClusters + ".p", "rb" ) )
    (MS, busToPosition, userToPosition, userToPositionPerClus) = getSM.getMatrices(train, "fact_ratings_matrix.txt", clusters)
    leng = len(MS)
    print "Done making. Writing to file..."
    positions = (busToPosition, userToPositionPerClus)
    pickle.dump(positions, open(folder+"/"+filePositions + ".p", "wb" ))
    print "Position dictionaries writen in: ", (filePositions + ".p")

    for i in range(leng):
        pickle.dump(MS[i], open(folder+"/"+fileMatrices + str(i) + ".p", "wb" ))
    print "Matrices writen in: ", (fileMatrices+"i.p"), " File formate MS[i]"
    return None
#clusterMatrices()

#print "factorizing matrices..."
sufix_matrix = "cluster_matrix_"
sufix_factors = "factors_"
#for i in range(clusters_k): factorizeMatrix(sufix_matrix + str(i), sufix_factors  + str(i))
def factorizeMatrix(fileMatrix, fileFactors, features = features, lamb = lamb, lrate = lrate, maxiters = maxiters, folder = folder):
    print "Factorizing..."
    matrix = pickle.load( open( folder+"/"+fileMatrix + ".p", "rb" ) ) 
    N = matrix.todok()
    #(W,H,mymu,bu,bb) = fact_bias.factorize_bias(N,features,lamb,lrate,maxiters)
    factors_and_stuff = fact_bias.factorize_bias(N,features,lamb,lrate,maxiters)
    #more_stuff = (factors_and_stuff,busToPosition, userToPositionPerClus)
    pickle.dump(factors_and_stuff, open(folder+"/"+fileFactors + ".p", "wb" ))

#for i in range(clusters_k): factorizeMatrix("cluster_matrix_" + str(i), "factors_" + str(i))

factor_files = ["factors_" + str(i) for i in range(clusters_k)]
def computeErrors(fileNames = factor_files , fileTest= "testData", filePositions = "postions", leng = clusters_k, folder = folder, test_train=test_train):
    print "Building prediction matrices..."
    
    def newList(n=5):
        return [0 for _ in range(n)]
    (W,H,mymu,bu,bb) = (newList(leng),newList(leng),newList(leng),newList(leng),newList(leng))
    predictionMatrices = [None for _ in range(leng)]
    for i in range(leng):
        #Load and unpack all the data:
        actors_and_stuff = pickle.load( open( folder+"/"+fileNames[i] + ".p", "rb" ) )
        (W[i],H[i],mymu[i],bu[i],bb[i]) = actors_and_stuff
        predictionMatrices[i] = mymu[i] + bu[i] + bb[i] + np.dot(W[i], H[i])

    print "computiung error..."
    total_tests = [0] * leng
    total_error = [0] * leng
    total_serror = [0] * leng
    unmatched_users = 0
    print "loading positions..."
    (busToPosition, userToPositionPerClus) = pickle.load( open( folder+"/"+filePositions + ".p", "rb" ) )
    print "loading Test data..."
    test = pickle.load( open( folder+"/"+fileTest + ".p", "rb" ) )
    #positions = (busToPosition, userToPositionPerClus)
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
    print "Rmse per cluster: ", [np.sqrt(total_serror[i]/float(total_tests[i])) for i in range(leng)]
    print "RMSE: ", np.sqrt(sum(total_serror)/float(sum(total_tests)))
    print "Parameters:"
    print "Clusters: ", leng , ", train/train: ", test_train-1, ", k: ", features, ", lambda: ", lamb, ", lrate: ", lrate, ", iterations: ", maxiters
    
    print "Done. Thank you for playing."
    
#computeErrors()




def computeOneError( clus_index, fileNames = factor_files , fileTest= "testData", filePositions = "postions", leng = clusters_k, folder = folder, test_train=test_train):
    print "Building prediction matrices..."
    
    def newList(n=5):
        return [0 for _ in range(n)]
    (W,H,mymu,bu,bb) = (newList(leng),newList(leng),newList(leng),newList(leng),newList(leng))
    predictionMatrices = [None for _ in range(leng)]
    for i in range(leng):
        if i == clus_index:
            #Load and unpack all the data:
            actors_and_stuff = pickle.load( open( folder+"/"+fileNames[i] + ".p", "rb" ) )
            (W[i],H[i],mymu[i],bu[i],bb[i]) = actors_and_stuff
            predictionMatrices[i] = mymu[i] + bu[i] + bb[i] + np.dot(W[i], H[i])

    print "computiung error..."
    total_tests = [0] * leng
    total_error = [0] * leng
    total_serror = [0] * leng
    unmatched_users = 0
    print "loading positions..."
    (busToPosition, userToPositionPerClus) = pickle.load( open( folder+"/"+filePositions + ".p", "rb" ) )
    print "loading Test data..."
    test = pickle.load( open( folder+"/"+fileTest + ".p", "rb" ) )
    #positions = (busToPosition, userToPositionPerClus)
    for (user, reviews) in test.iteritems():
        #row = userToPosition.get(user, None)
        for (bus, stars) in reviews.iteritems():
            (clusterN, index) = busToPosition[bus]
            if clus_index==clusterN:
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
    print "Average error of the cluster: ", (total_error[clus_index]/float(total_tests[clus_index]))
    print "Average serror of the cluster: ", (total_serror[clus_index]/float(total_tests[clus_index]))
    print "Rmse of the cluster: ", np.sqrt(total_serror[clus_index]/float(total_tests[clus_index]))
    print "Parameters:"
    print "Clusters: ", leng , ", train/train: ", test_train-1, ", k: ", features, ", lambda: ", lamb, ", lrate: ", lrate, ", iterations: ", maxiters
    
    print "Done. Thank you for playing."
    
#computeErrors()
