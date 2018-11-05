from math import sqrt

def normalizedPearson(col1,data1,col2,data2,L):
    d1,d2 = vect2dict(col1,data1,col2,data2)
    
    # Simple sums
    sum1 = sum(data1)
    sum2 = sum(data2)

    # Sum of the products
    pSum = sum([d1[i] * d2[i] for i in d1.viewkeys() & d2.viewkeys()])

    # Calculate r (Pearson score)
    num = pSum - (sum1 * sum2 / L)
    den = sqrt((sum1Sq - pow(sum1, 2) / L) * (sum2Sq - pow(sum2, 2) / L))
    if den == 0: return 0

    return 1 - num / den

# def euclideanDistance(v1, v2):
#     return sqrt (sum ([(x1 - x2)**2 for x1, x2 in zip(v1,v2)]))

# def cosineSimilarity(v1,v2):
#     # Sums of the squares
#     sum1Sq = sum([pow(v, 2) for v in v1])
#     sum2Sq = sum([pow(v, 2) for v in v2])

#     # Sum of the products
#     pSum = sum([x1 * x2 for x1, x2 in zip(v1,v2)])
    
#     num = pSum
#     den = sqrt(sum1Sq*sum2Sq)
#     return(1 - num / den)

def normalizedJaccardSimilarity(col1,data1,col2,data2):
     d1,d2 = vect2dict(col1,data1,col2,data2)
     return map(lambda x: x / (1 - x), [sum([d1[i] * d2[i] for i in d1.viewkeys() & d2.viewkeys()])])[0]

def normalization(v):
    sumSq = sum([pow(x, 2) for x in v])
    return v/pow(sumSq,1/2)

def normalizedCosineSimilarity(col1,data1,col2,data2):
    d1,d2 = vect2dict(col1,data1,col2,data2)
    dist = 1 - sum([d1[i] * d2[i] for i in d1.viewkeys() & d2.viewkeys()])
    if dist < 0: return 0
    return dist

def vect2dict(col1,data1,col2,data2):
    return dict(zip(col1,data1)),dict(zip(col2,data2))
