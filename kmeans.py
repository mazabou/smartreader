from math import sqrt
from PIL import Image,ImageDraw

def rotatematrix(data):
    newdata = []
    for i in range(len(data[0])):
        newrow = [data[j][i] for j in range(len(data))]
        newdata.append(newrow)
    return newdata


def kcluster(rows, distance=pearson, k=4):
    # Determine the minimum and maximum values for each point
    ranges = [(min([row[i] for row in rows]), max([row[i] for row in rows])) for i in range(len(rows[0]))]
    # Create k randomly placed centroids
    clusters = [[random.random() * (ranges[i][1] - ranges[i][0]) + ranges[i][0] for i in range(len(rows[0]))] for j in range(k)]

    lastmatches = None
    for t in range(100):
        print
        'Iteration %d' % t
        bestmatches = [[] for i in range(k)]
        # Find which centroid is the closest for each row
        for j in range(len(rows)):
            row = rows[j]
            bestmatch = 0
            for i in range(k):
                d = distance(clusters[i], row)
                if d < distance(clusters[bestmatch], row): bestmatch = i
            bestmatches[bestmatch].append(j)
        # If the results are the same as last time, this is complete
        if bestmatches == lastmatches: break
        lastmatches = bestmatches
        # Move the centroids to the average of their members
        for i in range(k):
            avgs = [0.0] * len(rows[0])
            if len(bestmatches[i]) > 0:
                for rowid in bestmatches[i]:
                    for m in range(len(rows[rowid])):
                        avgs[m] += rows[rowid][m]
                for j in range(len(avgs)):
                    avgs[j] /= len(bestmatches[i])
                clusters[i] = avgs
    return bestmatches



def scaledown(data, distance=pearson, rate=0.01):
    n = len(data)
    # The real distances between every pair of items
    realdist = [[distance(data[i], data[j]) for j in range(n)] for i in range(0, n)]
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


def draw2d(data, labels, jpeg='mds2d.jpg'):
    img = Image.new('RGB', (2000, 2000), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    for i in range(len(data)):
        x = (data[i][0] + 0.5) * 1000
        y = (data[i][1] + 0.5) * 1000
        draw.text((x, y), labels[i].encode('latin-1','ignore'), (0, 0, 0))
    img.save(jpeg, 'JPEG')