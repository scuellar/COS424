from gensim import corpora, models, similarities
import logging
import sys
import readYelp
import numpy
from scipy.io import mmwrite
from scipy.sparse import lil_matrix
from nltk.corpus import stopwords
from nltk.stem import porter, lancaster
import string
import pickle
import re

def posneg(filename, n=0):
    if n == 0:
        (l, d) = readYelp.readY('../yelp/yelp_academic_dataset_review.json')
    else:
        (l, d) = readYelp.readY('../yelp/yelp_academic_dataset_review.json', n)
    
    bus2index = {}
    businesses = 0
    
    user2index = {}
    users = 0
    
    for review in d:
        if review["business_id"] not in bus2index:
            bus2index[review["business_id"]] = businesses
            businesses += 1
    
        if review["user_id"] not in user2index:
            user2index[review["user_id"]] = users
            users += 1
    
    #outarray = numpy.zeros((businesses,users), dtype=numpy.int)
    matrix = lil_matrix((users, businesses))
    
    for review in d:
        answer = ""
        while answer != "y" and answer != "n":
            print review["stars"], review["text"]
            answer = raw_input()
    
        if answer == "y":
            matrix[user2index[review["user_id"]], bus2index[review["business_id"]]] = 1
        elif answer == "n":
            matrix[user2index[review["user_id"]], bus2index[review["business_id"]]] = -1
    
    mmwrite(filename, matrix)

def posneg2(filename, startPos, endPos):
    (l, d) = readYelp.readY('../yelp/yelp_academic_dataset_review.json', endPos) 

    outputreviews = []

    for review in d[startPos:endPos]:
        answer = ""
        while answer != "y" and answer != "n":
            print review["stars"], review["text"]
            answer = raw_input()
    
        if answer == "y":
            outputreviews.append(([review["user_id"], review["business_id"], 1]))
        elif answer == "n":
            outputreviews.append(([review["user_id"], review["business_id"], -1]))

    ofile = open(filename, 'wb')
    pickle.dump(outputreviews, ofile)
    ofile.close()
