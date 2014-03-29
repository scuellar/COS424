import csv
import numpy
from sklearn.cluster import KMeans
from sklearn.mixture import GMM
from random import shuffle
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

#with open('weatherdata/weatherdata_KNYC') as csvfile:
#with open('weatherdata/weatherdata_KSFO') as csvfile:
with open('finland.txt') as finfile:
    #reader = csv.reader(file, delimiter=' ')
    data = []
    for row in finfile:
        data.append([float(row.split()[0])/10000, float(row.split()[1])/10000])

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

    clusterer = GMM(n_components=6, init_params='wc', n_iter=300)
    clusterer.fit(data)

    [row.append(clusterer.predict([row])[0]) for row in data]

    clusters = []
    for c in range(0, 6):
        clusters.append([])
        for i in range(0, len(data)):
            if (data[i][2] == c):
                clusters[c].append(data[i])

    newdata = []
    for i in range(0, 6):
        newdata.append([])
        newdata[i] = map(list, zip(*clusters[i]))

    print clusterer.converged_
    print clusterer.weights_
    print clusterer.means_

    bmap = Basemap(projection='merc', lat_0 = 57, lon_0 = -135,
        resolution = 'h', area_thresh = 0.1,
        llcrnrlon=21.0, llcrnrlat=59.5,
        urcrnrlon=32.0, urcrnrlat=70.5)
    bmap.drawcoastlines()
    bmap.drawcountries()
    bmap.fillcontinents(color='coral')
    bmap.drawmapboundary()

    colours = ['bo', 'go', 'ro', 'yo', 'wo', 'co']

    for i in range(0, 6):
        lats = newdata[i][0]
        lons = newdata[i][1]

        x,y = bmap(lons, lats)
        #bmap.scatter(x, y, marker='o', c=newdata[i][2])#, markersize=10)
        bmap.plot(x, y, colours[i], markersize=4)#colours[i], markersize=4)

    plt.savefig("fig.png")
    plt.close()

    #fig, ax = plt.subplots()
    #plt.xlim([200000, 340000])
    #ax.scatter(newdata[1], newdata[0], c=newdata[2])
    
     
	
    #plt.show()
