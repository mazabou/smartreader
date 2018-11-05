from math import sqrt
import numpy as np
from similarityMeasures import normalizedCosineSimilarity
import random
from sklearn.decomposition import TruncatedSVD
from sklearn.manifold import TSNE


def scaledown(data, distance=normalizedCosineSimilarity, rate=0.01):
    n = len(data)
    # The real distances between every pair of items
    realdist = [[distance(data[i], data[j]) for j in range(n)] for i in range(n)]
    identical = [[i,j] for i in range(len(realdist)) for j in range(len(realdist)//2) if (i<>j and realdist[i][j]==0)]
    print identical 
    outersum = 0.0
    # Randomly initialize the starting points of the locations in 2D
    loc = [[random.random(), random.random()] for i in range(n)]
    fakedist = [[0.0 for j in range(n)] for i in range(n)]

    lasterror = None
    for m in range(0, 1000):
        # Find projected distances
        for i in range(n):
            for j in range(n):
                fakedist[i][j] = sqrt(sum([pow(loc[i][x] - loc[j][x], 2) for x in range(len(loc[i]))]))

        # Move points
        grad = [[0.0, 0.0] for i in range(n)]

        totalerror = 0
        for k in range(n):
            for j in range(n):
                if j == k: continue
                # The error is percent difference between the distances
                errorterm = (fakedist[j][k] - realdist[j][k]) / realdist[j][k]

                # Each point needs to be moved away from or towards the other
                # point in proportion to how much error it has
                grad[k][0] += ((loc[k][0] - loc[j][0]) / fakedist[j][k]) * errorterm
                grad[k][1] += ((loc[k][1] - loc[j][1]) / fakedist[j][k]) * errorterm

                # Keep track of the total error
                totalerror += abs(errorterm)
        #print(totalerror)

        # If the answer got worse by moving the points, we are done
        if lasterror and lasterror < totalerror: break
        lasterror = totalerror

        # Move each of the points by the learning rate times the gradient
        for k in range(n):
            loc[k][0] -= rate * grad[k][0]
            loc[k][1] -= rate * grad[k][1]

    return loc
	
def reduction(data):
	svd = TruncatedSVD(n_components=50, random_state=0)
	svd_tfidf = svd.fit_transform(data)
	tsne_model = TSNE(n_components=2, verbose=1, random_state=0)
	tsne_tfidf = tsne_model.fit_transform(svd_tfidf)
	return tsne_tfidf