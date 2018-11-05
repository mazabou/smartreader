from numpy import *
def difcost(a, b):
    dif = 0
    # Loop over every row and column in the matrix
    for i in range(shape(a)[0]):
        for j in range(shape(a)[1]):
            # Add together the differences
            dif += pow(a[i, j] - b[i, j], 2)
    return dif


def factorize(v, pc=10, iter=50):
    ic = shape(v)[0]
    fc = shape(v)[1]
    # Initialize the weight and feature matrices with random values 
    w=matrix([[random.random() for j in range(pc)] for i in range(ic)]) 
    h=matrix([[random.random() for i in range(fc)] for i in range(pc)])

    # Perform operation a maximum of iter times
    for i in range(iter):
        wh = w * h

        # Calculate the current difference
        cost = difcost(v, wh)

        if i % 10 == 0: print cost

        # Terminate if the matrix has been fully factorized
        if cost == 0: break

        # Update feature matrix
        hn = (transpose(w) * v)
        hd = (transpose(w) * w * h)

        h = matrix(array(h) * array(hn) / array(hd))

        # Update weights matrix
        wn = (v * transpose(h))
        wd = (w * h * transpose(h))

        w = matrix(array(w) * array(wn) / array(wd))
    return w, h

def showfeatures(w,h,titles,wordvec,out='features.txt'):
    outfile=file(out,'w')
    pc,wc=shape(h)
    toppatterns=[[] for i in range(len(titles))]
    patternnames=[]
    # Loop over all the features
    for i in range(pc):
        slist=[]
        # Create a list of words and their weights
        for j in range(wc):
            slist.append((h[i,j],wordvec[j])) 

        # Reverse sort the word list 
        slist.sort( )
        slist.reverse( )
        # Print the first six elements
        n=[s[1] for s in slist[0:6]]
        print(str(n))
        patternnames.append(n)
        # Create a list of articles for this feature
        flist=[]
        for j in range(len(titles)):
          # Add the article with its weight
          flist.append((w[j,i],titles[j]))
          toppatterns[j].append((w[j,i],i,titles[j]))
        # Reverse sort the list 
        flist.sort( ) 
        flist.reverse( )
        # Show the top 3 articles
        for f in flist[0:3]:
          print(str(f))
        #outfile.write('\n')
    outfile.close()
    # Return the pattern names for later use 
    return toppatterns,patternnames