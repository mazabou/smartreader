import parser
from preprocess import *

par = parser.Parser()
par.parse()
rownames, colnames, data = readfile()
data,colnames = pruning(data,colnames,0.05,0.9)
data=tfidf(data)
writefile(rownames, colnames, data)


import HAC
analyser = HAC.HAC()
clust = analyser.hcluster(data)

clust = analyser.hcluster(data,cosineSimilarity)

analyser.printclust(clust,rownames)


from kmeans import *
clusters = kcluster(data)
printcluster(clusters,rownames)



import NMF
import numpy

v=numpy.matrix(data)
weights,feat=NMF.factorize(v,pc=20,iter=50)
topp,pn= NMF.showfeatures(weights,feat,rownames,colnames)