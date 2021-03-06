from math import sqrt
import numpy as np
from similarityMeasures import normalizedCosineSimilarity
import random
import pandas as pd
import bokeh.plotting as bp
from bokeh.models import HoverTool, BoxSelectTool
from bokeh.plotting import figure, show, output_file

def kcluster(cols,data,L, distance=normalizedCosineSimilarity, k=4):

    # Determine the minimum and maximum values for each point
    ranges = [[1, 0] for i in range(L)]
    for col,row in zip(cols,data):
        for i in range(len(col)):
            if row[i] > ranges[col[i]][1]: ranges[col[i]][1] = row[i]
            if row[i] < ranges[col[i]][0]: ranges[col[i]][0] = row[i]

    # Create k randomly placed centroids
    clusters = [[random.random() * (ranges[i][1] - ranges[i][0]) + ranges[i][0] for i in range(L)] for j in range(k)]
    clusters_col = [list(range(L)) for i in range(len(data))]

    lastmatches = None
    for t in range(100):
        print('Iteration %d' % t)
        bestmatches = [[] for i in range(k)]
        # Find which centroid is the closest for each row
        for j in range(len(data)):
            col = cols[j]
            row = data[j]
            bestmatch = 0
            bestdistance = 2
            for i in range(k):
                d = distance(clusters_col[i],clusters[i],col, row)
                if d < bestdistance: bestmatch, bestdistance = i, d
            bestmatches[bestmatch].append(j)
        # If the results are the same as last time, this is complete
        if bestmatches == lastmatches: break
        lastmatches = bestmatches
        # Move the centroids to the average of their members
        for i in range(k):
            avgs = [0.0] * L
            count = [0] * L
            if len(bestmatches[i]) > 0:
                for rowid in bestmatches[i]:
                    col = cols[rowid]
                    row = data[rowid]
                    for j in range(len(col)):
                        avgs[col[j]] += row[j]
                        count[col[j]] += 1
            clusters[i] = [y != 0 and x/y or 0 for x,y in zip(avgs,count)]
    #Calculating Calinski and Harabaz Index
    #c, center of E
    #c = [np.mean(L) for L in zip(*clusters)]
    #W_k = sum([sum([distance(clusters_col[i],clusters[i],cols[j], data[j])**2 for j in bestmatches[i]]) for i in range(k)])
    #B_k = sum([distance(clusters_col[i],clusters[i],clusters_col[i],c)*len(bestmatches[i]) for i in range(k)])
    #s = ((B_k)/(W_k))*((L-k)/(k-1))
    return bestmatches, clusters, clusters_col

def optimized_kmeans(rows, distance=normalizedCosineSimilarity):
    list_data = []
    for k in range(2,50):
        print("------> k = " + str(k))
        bestmatches, s = kcluster(rows, distance=pearson, k=k)
        for i in range(5):
            bestmatches_n, s_n = kcluster(rows, distance=pearson, k=k)
            print str(i)+': '+str(s_n)
            if s_n > s:
                s = s_n
                bestmatches = bestmatches_n
        list_data.append([bestmatches, s])
        if k > 4:
            if list_data[-1][1] < list_data[-2][1]:
                break
    return k, max(list_data, key=lambda x: x[1])

def visualize(loc,bestmatches,articledf):
    output_file("test.html")
    rownames = articledf.title
    colormap = np.array(["#6d8dca", "#69de53", "#723bca", "#c3e14c", "#c84dc9", "#68af4e", "#6e6cd5","#e3be38", "#4e2d7c", "#5fdfa8", "#d34690", "#3f6d31", "#d44427", "#7fcdd8", "#cb4053", "#5e9981","#803a62", "#9b9e39", "#c88cca", "#e1c37b", "#34223b", "#bdd8a3", "#6e3326", "#cfbdce", "#d07d3c","#52697d", "#7d6d33", "#d27c88", "#36422b", "#b68f79"])
    plot_kmeans = bp.figure(plot_width=700, plot_height=600, title="KMeans clustering of the news",tools="pan,wheel_zoom,box_zoom,reset,hover,previewsave",x_axis_type=None, y_axis_type=None, min_border=1)
    kmeans_df = pd.DataFrame(loc, columns=['x', 'y'])
    cluster_list = [0]*len(rownames)
    for i in range(1,len(bestmatches)):
        for j in bestmatches[i]:
            cluster_list[j]=i
    kmeans_df['cluster'] = pd.DataFrame(cluster_list)
    kmeans_df['title'] = pd.DataFrame(rownames)
    kmeans_df['color'] = colormap[cluster_list]
    kmeans_df['source'] = articledf.source
    plot_kmeans.scatter(x='x', y='y',color='color', source=kmeans_df)
    hover = plot_kmeans.select(dict(type=HoverTool))
    hover.tooltips={"title": "@title","cluster":"@cluster","source":"@source"}
    show(plot_kmeans)

def printcluster(clusters,rownames):
    for c in kcluster:
        for article in [rownames[r] for r in c]:
            print(article)
        print('-------------------------------')