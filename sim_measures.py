__author__ = 'SCKobayashi'

import numpy

def euclideanDistance(a,b):
    D=0
    for i in range(len(a)):
        D=(a[i]-b[i])**2
    D = D**(1/2)
    return D

def cosineSimilarity(a,b):
    D = numpy.dot(a,b)/(numpy.dot(a,a)*numpy.dot(b,b))**(1/2)
    return D

def jaccardSimilarity(a,b):
    D = numpy.dot(a,b)/(numpy.dot(a,a)+numpy.dot(b,b)-numpy.dot(a,b))
    return D

def normalization(a):
    a = a/numpy.dot(a,a)**(1/2)
    return a

def normalizedCosineSimilarity(a,b):
    D = numpy.dot(a,b)
    return D

print(jaccardSimilarity([1,1],[1,0]))
print(normalization([3,4,2]))

