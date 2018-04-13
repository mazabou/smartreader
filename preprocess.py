import numpy as np

def readfile(filename='articlewordmatrix.txt'):
    fileInfo=open('articlesmetadata.txt')
    fileMatrix=open(filename)

    lines = [line for line in fileMatrix]
    # First line is the column titles
    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        # First column in each row is the rowname
        rownames.append(p[0])
        # The data for this row is the remainder of the row
        data.append([float(x) for x in p[1:]])
    sources = []
    authors = [] 
    url = []
    #published = []
    #for line in fileInfo:
    #    p = line.strip().split('\t')
    #    if p == ['error']:
    #        p = ['None']*4
    #    sources.append(p[1])
    #    authors.append(p[2])
    #    url.append(p[3])
       #published.append(p[4])
    fileMatrix.close()
    fileInfo.close()
    return rownames, colnames, data

def writefile(rownames, colnames, data):
    fileMatrix=open('articlewordmatrix_processed.txt','w')

    fileMatrix.write('Article')
    for word in colnames: fileMatrix.write('\t%s' % word)
    fileMatrix.write('\n')

    for i in range(len(rownames)):
        fileMatrix.write(rownames[i])
        row = '\t' + '\t'.join(map(str, data[i])) + '\n'
        fileMatrix.write(row)
    
    fileMatrix.close()


#Convert the data matrix to a tf matrix
def tf(data):
    return [termfreq(v) for v in data]

#Convert the data matrix to a tf-idf matrix
def tfidf(data):
    data_tf = tf(data)
    idf_vec = invdocfreq(data)
    return [[c * idf for c, idf in zip(v,idf_vec)] for v in data_tf]

#term frequency
def termfreq(v):
    return [c != 0 and 1 + np.log(c) or 0 for c in v]

#inverse document frequency	
def docap(data):
    N = len(data)
    return [o/N for o in [sum([c and 1 for c in x]) for x in zip(*data)]]

def invdocfreq(data):
    return [np.log(1/x) for x in docap(data)]

def pruning(data,colnames,lowerthreshold,higherthreshold):
    matrix, words = data[:], colnames[:]
    apvec = docap(matrix)
    wordstodel = []
    for i in range(len(apvec)):
        if not lowerthreshold < apvec[i] < higherthreshold:
            wordstodel = [i] + wordstodel # or append than reverse?
    for wordid in wordstodel:
        for v in matrix:
            del v[wordid]
        del words[wordid]
    return matrix,words

def truncation(data):
    pass

