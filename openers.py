import pandas as pd
from scipy.sparse import csr_matrix

def open_words():
    df = pd.read_csv('words.csv')
    df.loc[0]=range(df.shape[1])
    return df.to_dict('records')[0]

def open_matrix():
    file = open('data.csv','r')
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

def open_data():
    file = open('data.csv','r')
    lines = [line for line in file]
    file.close()

    col = []
    data = []
    for i in range(len(lines)/2):
        col.append(map(int,lines[2*i].strip().split(',')))
        data.append(map(float,lines[1+2*i].strip().split(',')))

    return col,data


def open_metadata():
	return pd.read_csv('metadata.csv')
