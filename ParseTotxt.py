class ParseTotxt:
	def __init__(self,update):
	    print 'Parsed data will be saved in articlesmetadata.txt and articlewordmatrix.txt'
	    self.wordcounts={}
	    self.articleList=[]
	    self.articles=[]
	    if update:
	        print 'Loading previous data set //update'
	        fileInfo=open('articlesmetadata.txt')
	        self.articles = [line for line in fileInfo]
	        fileInfo.close()

	        self.articleList, colnames, data = self.readfile()
	        for article,count in zip(self.articleList,data):
	            self.wordcounts[article]=dict(zip(colnames,count))


	# def init(self):
	# 	print 'Parsed data will be saved in articlesmetadata.txt and articlewordmatrix.txt'
	# 	self.wordcounts={}
	#     self.articleList=[]
	#     self.articles=[]

	# def load(self):
	# 	print 'Parsed data is added to articlesmetadata.txt and articlewordmatrix.txt'

	def add(self,title, source, author, url, published, words):
	        self.articleList.append(title)

	        self.articles.append(title+"\t"+source+"\t"+author+"\t"+url+"\t"+published)

	        wc={}
	        for word in words:
	            wc.setdefault(word,0)
	            wc[word]+=1
	        self.wordcounts[title]=wc

	def isindexed(self,title):
	        return title in self.articleList
	    
	def commit(self):
	    print 'Saving collected data...'
	    fileInfo=open('articlesmetadata.txt','w')
	    fileMatrix=open('articlewordmatrix.txt','w')
	    wordlist=[]
	    for wc in self.wordcounts.values():
	        for word in wc.keys(): #set?
	            if word not in wordlist:
	                wordlist.append(word)

	    self.fileMatrix.write('Article')
	    for word in wordlist: self.fileMatrix.write('\t%s' % word)
	    self.fileMatrix.write('\n')
	    for article, wc in self.wordcounts.items():
	        #deal with unicode outside the ascii range
	        article=article.encode('ascii','ignore')
	        self.fileMatrix.write(article)
	        for word in wordlist:
	            if word in wc: self.fileMatrix.write('\t%d' % wc[word])
	            else: self.fileMatrix.write('\t0')
	        self.fileMatrix.write('\n')
	        
	    for d in self.articles:
	        try:
	            fileInfo.write(d)
	        except:
	            fileInfo.write('error')
	        fileInfo.write('\n')
	    fileMatrix.close()
	    fileInfo.close()
	    print 'Data saved in articlewordmatrix.txt and articlesmetadata.txt'

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
	    fileMatrix.close()
	    fileInfo.close()
	    return rownames, colnames, data