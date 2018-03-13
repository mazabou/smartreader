class ParseTotxt:
	def __init__(self):
	    print 'Parsed data will be saved in articlesmetadata.txt and articlewordmatrix.txt'
	    self.wordcounts={}
	    self.articleList=[]
	    self.articles=[]

	# def init(self):
	# 	print 'Parsed data will be saved in articlesmetadata.txt and articlewordmatrix.txt'
	# 	self.wordcounts={}
	#     self.articleList=[]
	#     self.articles=[]

	# def load(self):
	# 	print 'Parsed data is added to articlesmetadata.txt and articlewordmatrix.txt'

	def add(self,title, source, author, url, published, words):
	        self.articleList.append(url)

	        self.articles.append(title+"\t"+source+"\t"+author+"\t"+url+"\t"+published)

	        wc={}
	        for word in words:
	            wc.setdefault(word,0)
	            wc[word]+=1
	        self.wordcounts[url]=wc

	def isindexed(self,url):
	        return url in self.articleList
	    
	def commit(self):
	    self.fileInfo=open('articlesmetadata.txt','w')
	    self.fileMatrix=open('articlewordmatrix.txt','w')
	    wordlist=[]
	    for wc in self.wordcounts.values():
	        for word in wc.keys(): #set?
	            if word not in wordlist:
	                wordlist.append(word)

	    for word in wordlist: self.fileMatrix.write('\t%s' % word)
	    self.fileMatrix.write('\n')
	    for article, wc in self.wordcounts.items():
	        #deal with unicode outside the ascii range
	        #blog=blog.encode('ascii','ignore')
	        self.fileMatrix.write(article)
	        for word in wordlist:
	            if word in wc: self.fileMatrix.write('\t%d' % wc[word])
	            else: self.fileMatrix.write('\t0')
	        self.fileMatrix.write('\n')
	    for d in self.articles:
	        try:
	            self.fileInfo.write(d)
	        except:
	            self.fileInfo.write('error')
	        self.fileInfo.write('\n')
	    self.fileMatrix.close()
	    self.fileInfo.close()

	def readfile(self):
	    fileInfo=open('articlesmetadata.txt')
	    fileMatrix=open('articlewordmatrix.txt')
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
	    return rownames, colnames, data