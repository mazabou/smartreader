from math import sqrt

def pearson(v1, v2):
    # Simple sums
    sum1 = sum(v1)
    sum2 = sum(v2)

    # Sums of the squares
    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])

    # Sum of the products
    pSum = sum([x1 * x2 for x1, x2 in zip(v1,v2)])

    # Calculate r (Pearson score)
    num = pSum - (sum1 * sum2 / len(v1))
    den = sqrt((sum1Sq - pow(sum1, 2) / len(v1)) * (sum2Sq - pow(sum2, 2) / len(v1)))
    if den == 0: return 0

    return 1 - num / den

def euclideanDistance(v1, v2):
    return sqrt (sum ([(x1 - x2)**2 for x1, x2 in zip(v1,v2)]))

def cosineSimilarity(v1,v2):
    # Sums of the squares
    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])

    # Sum of the products
    pSum = sum([x1 * x2 for x1, x2 in zip(v1,v2)])
    
    num = pSum
    den = sqrt(sum1Sq*sum2Sq)
    return(1 - num / den)

def jaccardSimilarity(v1,v2):
    # Sums of the squares
    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])

    # Sum of the products
    pSum = sum([x1 * x2 for x1, x2 in zip(v1,v2)])

    return pSum / ( sum1Sq*Sum2Sq - pSum)

def normalization(v):
    sumSq = sum([pow(x, 2) for x in v])
    return v/pow(sumSq,1/2)

def normalizedCosineSimilarity(v1,v2):
    return sum([x1 * x2 for x1, x2 in zip(v1,v2)])
