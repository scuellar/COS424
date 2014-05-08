from gensim import corpora, models, similarities
import logging
import sys
import readYelp
import numpy
from nltk.corpus import stopwords
from nltk.stem import porter, lancaster
import string

import re

def remove_punctuation(text):
    return re.sub(r'[^\w\s]','',text)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def buildCorpus(dictname, corpname, tfidfname, n=-1, stem=True, punctuation=True):
    stoplist = set(stopwords.words('english'))
    stemmer = porter.PorterStemmer()
    #stemmer = lancaster.LancasterStemmer()

    if (n==-1):
        (l, d) = readYelp.readY('../yelp/yelp_academic_dataset_review.json')
    else:
        (l, d) = readYelp.readY('../yelp/yelp_academic_dataset_review.json', n)
    
    print "make lower case words"
    if stem:
        unfilteredtexts = [[stemmer.stem(word) for word in text['text'].split()] for text in d]
        if punctuation:
            texts = [[word.lower() for word in reviewtext if word.lower() not in stoplist] for reviewtext in unfilteredtexts]
        else:
            texts = [[remove_punctuation(word).lower() for word in reviewtext if word.lower() not in stoplist] for reviewtext in unfilteredtexts]
    else:
        if punctuation:
            texts = [[word.lower() for word in text['text'].split() if word.lower() not in stoplist] for text in d]
        else:
            texts = [[remove_punctuation(word).lower() for word in text['text'].split() if word.lower() not in stoplist] for text in d]

    
    #print texts[0:100]
    
    print "make dictionary"
    dictionary = corpora.Dictionary(texts)
    dictionary.save(dictname)
    
    print "make corpus"
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize(corpname, corpus)
    
    #mmcorpus = corpora.MmCorpus('corpus.mm')
    
    tfidf = models.TfidfModel(corpus)
    tfidfCorpus = tfidf[corpus]
    corpora.MmCorpus.serialize(tfidfname, tfidfCorpus)

#index = similarities.SpareMatrixSimilarity(tfidf[corpus], num_features=15)

#sims = index[tfidf[vec]]

def performlda(dictname, corpusname):
    dictionary = corpora.Dictionary.load(dictname)
    corpus = corpora.MmCorpus(corpusname)
    print "latent dirichlet allocate"
    #lsi = models.lsimodel.LsiModel(corpus=tfidfCorpus, id2word=dictionary, num_topics=10)
    #lsi.print_topics(10)
    
    lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=20, update_every=1, chunksize=10000, passes=10)
    lda.print_topics(20)
