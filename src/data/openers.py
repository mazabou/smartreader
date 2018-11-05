import pandas as pd
from scipy.sparse import csr_matrix

def open_words(name = 'words.csv'):
    df = pd.read_csv(name)
    df.loc[0]=range(df.shape[1])
    return df.to_dict('records')[0]

def open_matrix(name = 'data.csv'):
    file = open(name,'r')
    lines = [line for line in file]
    file.close()

    col = []
    row = []
    data = []
    for i in range(len(lines)/2):
        l = map(int,lines[2*i].strip().split(','))
        col.extend(l)
        row.extend([i for j in range(len(l))])
        data.extend(map(int,lines[1+2*i].strip().split(',')))

    return csr_matrix((data, (row, col)))

def open_data(name = 'data.csv'):
    file = open(name,'r')
    lines = [line for line in file]
    file.close()

    col = []
    data = []
    for i in range(len(lines)/2):
        try:
            col.append(map(int,lines[2*i].strip().split(',')))
            data.append(map(float,lines[1+2*i].strip().split(',')))
        except:
            print i
    return col,data


def open_metadata(name = 'metadata.csv'):
	return pd.read_csv(name,index_col=0)
