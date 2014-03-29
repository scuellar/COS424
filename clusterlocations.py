import csv
import numpy
from sklearn.cluster import KMeans
from sklearn.mixture import GMM
from random import shuffle
import matplotlib.pyplot as plt

#with open('weatherdata/weatherdata_KNYC') as csvfile:
#with open('weatherdata/weatherdata_KSFO') as csvfile:
with open('finland.txt') as finfile:
    #reader = csv.reader(file, delimiter=' ')
    data = []
    for row in finfile:
        data.append([float(row.split()[0]), float(row.split()[1])])

    shuffle(data)

    #cluster = KMeansClusterer(5, euclidean_distance)
    #cluster.cluster(data)

    #for fold in range(0, 5):
    #    foldItems = []
    #    loo = []
    #    for i in range(0, len(data)):
    #        if (i % 5 == fold):
    #            loo.append(data[i])
    #        else:
    #            foldItems.append(data[i])

    #    clusterer = GMM(n_components=4, init_params='wc', n_iter=300)
    #    clusterer.fit(foldItems)

    #    clusterer.score_samples(loo)

    #    print clusterer.converged_
    #    print clusterer.weights_
    #    print clusterer.means_

    clusterer = GMM(n_components=5, init_params='wc', n_iter=300)
    clusterer.fit(data)

    [row.append(clusterer.predict([row])[0]) for row in data]

    newdata = map(list, zip(*data))

    print clusterer.converged_
    print clusterer.weights_
    print clusterer.means_

    fig, ax = plt.subplots()
    plt.xlim([200000, 340000])
    ax.scatter(newdata[1], newdata[0], c=newdata[2])
    plt.show()
