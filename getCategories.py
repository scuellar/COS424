import operator
import readYelp
import justTry
from sklearn.cluster import KMeans

"""This provides the categories named by mor than k businesses"""
def getCategoriesGT(i=0, k = 300):
    #get the data
    (l, d) = readYelp.readY('../yelp/yelp_academic_dataset_business.json', i)

    catList = [ bus.get("categories", []) for bus in d]
    countCats = {}
    for bus_cats in catList:
        for cat in bus_cats:
            countCats[cat] = countCats.get(cat, 0) + 1

    sorted_count = sorted(countCats.iteritems(), key=operator.itemgetter(1))
    top_cats = [ cat.encode('utf-8') for (cat,num) in sorted_count if num > k]
    return top_cats

"""This provides the top n categories"""
def getCategoriesTOP(i=0, n = 32):
    #get the data
    (l, d) = readYelp.readY('../yelp/yelp_academic_dataset_business.json', i)

    catList = [ bus.get("categories", []) for bus in d]
    countCats = {}
    for bus_cats in catList:
        for cat in bus_cats:
            countCats[cat] = countCats.get(cat, 0) + 1

    sorted_count = sorted(countCats.iteritems(), key=operator.itemgetter(1))
    if len(sorted_count)> 100:
        top_cats = sorted_count[-n +1: len(sorted_count)]        
        return [cat for (cat, num) in top_cats]
    else:
        return [cat for (cat, num) in sorted_count]
