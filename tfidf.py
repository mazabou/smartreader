__author__ = 'SCKobayashi'
import math
import numpy

#term frequency

def termFreq(occvector):
#en supposant qu'on ait en entree un vecteur occurence de mots pour chaque article
    for i in range(len(occvector)):
        if occvector[i] != 0:
            occvector[i] = 1 + math.log(occvector[i])
    return occvector

#inverse document frequency

def invDocFreq(N,df):
    return math.log(N/df)

def tfidf(occvector,df,N):
#en supposant que df soit un vecteur de nombre de document contenant au moins une fois le mot, N le nombre total de documents
    occvector = termFreq(occvector)
    occvector = numpy.dot(occvector, math.log(df/N))
    return occvector


dic={'arbre':2,'lol':0,'nullissime':1,"occurnece semi-entiere":0.5}
print(termFreq(dic))
