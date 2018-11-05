import numpy as np
from math import sqrt 

#Convert the data matrix to a tf matrix
def tf(data):
    return [termfreq(v) for v in data]

#Convert the data matrix to a tf-idf matrix
def tfidf(data,col,L):
    data_tf = tf(data)
    idf_vec = invdocfreq(col,L)
    return [[c * idf for c, idf in zip(v,idf_vec)] for v in data_tf]

#term frequency
def termfreq(v):
    return [c != 0 and 1 + np.log(c) or 0 for c in v]

#document frequency	
def docap(col,L):
    # L number of words
    apvec = [0]*L
    for v in col:
        for i in v:
            apvec[i]+=1
    return apvec

def invdocfreq(col,L):
    N = len(col)
    return [np.log(N/float(x)) for x in docap(col,L)]

def pruning(data,col,colnames,lowerthreshold,higherthreshold):
    data1, col1 = [],[]
    print 'Computing the document frequency vector...'
    apvec = docap(col,len(colnames))
    wordstokeep = []

    print 'Looking for words to keep...'
    for i in range(len(apvec)):
        if lowerthreshold*len(data) < apvec[i] < higherthreshold*len(data):
            wordstokeep.append(i)

    print 'Generating new matrix...'
    mapper = dict(zip(wordstokeep,range(len(wordstokeep))))

    for d,c in zip(data,col):
        try:
            T1,T2 = zip(*filter(lambda x: x[0] in wordstokeep,zip(c,d)))
            col1.append(map(lambda x: mapper[x], list(T1)))
            data1.append(list(T2))
        except:
            print "no!"

    return data1, col1, wordstokeep
    

def truncation(data):
    pass

def normalization(data):
    return [normalization_v(v) for v in data]

def normalization_v(v):
    sumSq = sum([pow(x, 2) for x in v])
    return [x/sqrt(sumSq) for x in v]
