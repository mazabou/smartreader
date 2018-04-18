import pandas as pd

class ParseTotxt:
	def __init__(self):
	    self.wordcounts={}
	    self.articles=[]
	    self.articledf = pd.DataFrame(columns=["title","source","Category","author","url","published"])

	    # if update:
	    #     print 'Loading previous data set //update'
	    #     fileInfo=open('articlesmetadata.txt')
	    #     self.articles = [line for line in fileInfo]
	    #     fileInfo.close()

	    #     self.articles, colnames, data = self.readfile()
	    #     for article,count in zip(self.articles,data):
	    #         self.wordcounts[article]=dict(zip(colnames,count))


	def add(self,title, source, category, author, url, published, words):
	    last = len(self.articledf)
	    title = title.encode('ascii','ignore')
	    self.articledf.loc[last] = [title,source,category,author.encode('ascii','ignore'),url,published]
	    
	    self.articles.append(title)

	    wc={}
	    for word in words:
	        wc.setdefault(word,0)
	        wc[word]+=1
	    self.wordcounts[title]=wc

	def isindexed(self,title):
	        return title in self.articles
	    
	def commit(self,dataFilename,infoFilename):
	    print 'Saving collected data...'

	    # Saving the words in the words file
	    wordFile = open('words.csv','w')
	    wordlist = []
	    for wc in self.wordcounts.values():
	        for word in wc.keys(): #set?
	            if word not in wordlist:
	                wordlist.append(word)
	    wordFile.write(','.join(wordlist))
	    wordFile.close()

	    #Saving article metadata
	    self.articledf.to_csv(infoFilename)

	    #Saving article data
	    dataFile=open(dataFilename,'w')
	    for article in self.articledf.title:
	        #article=article.encode('ascii','ignore')
	        #dataFile.write(article)
	        wc = self.wordcounts[article]
	        col = []
	        data = []
	        for i in range(len(wordlist)):
	            if wordlist[i] in wc:
	                col.append(i)
	                data.append(wc[wordlist[i]])
	        dataFile.write(','.join(map(str,col)))
	        dataFile.write('\n')
	        dataFile.write(','.join(map(str,data)))
	        dataFile.write('\n')
	    dataFile.close()
	    print 'Data saved'