import parser
from preprocess import *

par = parser.Parser()
par.parse()
rownames, colnames, data = readfile()
data,colnames = pruning(data,colnames,0.05,0.9)
data=tfidf(data)
writefile(rownames, colnames, data)