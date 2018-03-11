import urllib2
import feedparser
from bs4 import BeautifulSoup
import sqlite3 as sqlite
import re
import os

# Create a list of words to ignore
ignorewords=set(['the','of','to','and','a','in','is','it'])

class Parser:
    def __init__(self,filename="parsedData.txt",rssFile="rssList.txt"):
        # Set up the output
        fileExtension = re.findall(r".*?\.(\w+)",filename)[0]

        if fileExtension not in ["txt","db"]:
            filename, fileExtension = "parsedData.txt","txt"
            print "Error with the filename, parsedData.txt is chosen instead as the output file"
        else: 
            print filename+"is the output file"

        opt = {"txt":(self.initTXT,self.addToTXT,self.isindexedTXT,self.commitTXT),"db":(self.initDB,self.addToDB,self.isindexedDB,self.commitDB)}
        self.initialize,self.add,self.isindexed,self.commit = opt[fileExtension]

        self.initialize(filename)

        # Pulling the data from the rss file
        self.rssList = {} 
        print "Pulling the RSS Feeds list from " + rssFile
        self.setFeedList(rssFile)


    def initTXT(self,filename):
        self.fileInfo=open(filename,'w')
        self.file=open("matrix_"+filename,'w')
        self.wordcounts={}
        self.articleList=[]
        self.articles=[]

    def initDB(self,filename):
        print "Connecting to the database "+dbname
        self.con = sqlite.connect(dbname)
        self.rssList = {}
        print "Extracting rss feeds from "+filename


    def setFeedList(self,filename):
       file = open(filename)
       for line in file: #? for line in file
            rssName, rssFeed = line.strip().split(' ')
            self.rssList[rssName] = rssFeed
       file.close()

    def parse(self):
        for rssName in self.rssList.keys():
            rssFeed = self.rssList[rssName]
            rss = feedparser.parse(rssFeed)
            print "Connecting to "+rssName
            print "--------------"
            for entry in rss.entries:
                title = entry["title"]
                try:
                    author = entry["author"]
                except:
                    author = "None"
                try:
                    published = str(entry["published_parsed"])
                except:
                    published = "None"
                url = entry["link"]
                try:
                    c = urllib2.urlopen(url)
                except:
                    print "Could not open %s" % url
                    continue
                soup = BeautifulSoup(c.read(),"html.parser")
                self.addtoindex(url, soup, title, rssName, author, published)
        self.commit()

    # Index an individual page
    def addtoindex(self, url, soup, title, source, author, published):
            if self.isindexed(url): return
            print 'Indexing ' + url
            # Get the individual words
            if source[:2] == "NYT":
                text = self.getArticleNYT(soup)
            else:
                text = self.getArticleP(soup)
            text = text.encode('utf-8') #probleme d'encodage rencontre

            ## Il faut supprimer ou renommer le repertoire src
            s = title.encode('utf-8')
            s = str(s).strip().replace(' ', '_')
            filename = re.sub(r'(?u)[^-\w.]', '', s)
            filename = './src/'+ filename + '.txt'
            try:
                file = open(filename,'w')
                file.write(text)
                file.close()
            except:
                print "Error, filename = "+ filename
                filename = "None"
            words = self.separatewords(text)
            self.add(title, source, author, url, published, filename, words)
            

    def addToDB(self,title, source, author, url, published, filename, words):
            # Get the URL id
            cur = self.con.execute("insert into articleList (title,source,author,link,published,file) values (?, ?, ?, ?, ?, ?)", (title, source, author, url, published, filename))
            articleid = cur.lastrowid

            # Link each word to this url
            for word in words:
                if word in ignorewords: continue
                cur = self.con.execute("select rowid from wordList where word='%s'" % word)
                res = cur.fetchone()
                if res == None:
                    cur = self.con.execute("insert into wordList (word) values ('%s')" % word)
                    wordid = cur.lastrowid
                else:
                    wordid = res[0]
                cur = self.con.execute("select rowid from wordCount where articleid=%d and wordid=%d" %(articleid, wordid))
                res = cur.fetchone()
                if res == None:
                    self.con.execute("insert into wordCount(articleid,wordid,wcount) values (%d,%d,%d)" % (articleid, wordid, 1))
                else:
                    self.con.execute("update wordCount set wcount = wcount + 1 where articleid=%d and wordid=%d" %(articleid, wordid))

    def addToTXT(self,title, source, author, url, published, filename,words):
        self.articleList.append(url)

        self.articles.append(title+"\t"+source+"\t"+author+"\t"+url+"\t"+published+"\t"+filename)

        wc={}
        for word in words:
            wc.setdefault(word,0)
            wc[word]+=1
        self.wordcounts[url]=wc

# Extract the text from an HTML page (no tags)
    def getArticleNYT(self, soup):
        matches = soup.findAll("p", {"class": "story-body-text story-content"})
        resultText = ''
        for p in matches:
            text = self.getText(p)
            resultText += text + '\n'
        return resultText

    def getArticleP(self,soup):
        matches = soup.findAll("p")
        resultText = ''
        for p in matches:
            text = self.getText(p)
            resultText += text + '\n'
        return resultText

    def getText(self,soup):
        v = soup.string
        if v == None:
            c = soup.contents
            resulttext = ''
            for t in c:
                subtext = self.getText(t)
                resulttext += subtext + ' '
            return resulttext
        else:
            return v.strip()

# Separate the words by any non-whitespace character
    def separatewords(self,text):
        splitter = re.compile(r'\W*')
        return self.filter([s.lower() for s in splitter.split(text) if s != ''])

    def filter(self,words):
        return [word for word in words if (len(word)>1 and word.isalpha())] #list comprehension

# Return true if this url is already indexed
    def isindexedDB(self,url):
        u = self.con.execute("select rowid from articleList where link='%s'" % url).fetchone()
        return (u != None)

    def isindexedTXT(self,url):
        return url in self.articleList

    def commitDB(self):
        self.con.commit()

    def commitTXT(self):
        apcount={}
        for wc in self.wordcounts.values():
            for word,count in wc.items():
                apcount.setdefault(word,0)
                if count>1:
                    apcount[word]+=1

        wordlist=[]
        for w,bc in apcount.items():
            frac=float(bc)/len(self.articleList)
            if frac>0.1 and frac<0.5: wordlist.append(w)

        self.file.write('Article')
        for word in wordlist: self.file.write('\t%s' % word)
        self.file.write('\n')
        for article, wc in self.wordcounts.items():
            #deal with unicode outside the ascii range
            #blog=blog.encode('ascii','ignore')
            self.file.write(article)
            for word in wordlist:
                if word in wc: self.file.write('\t%d' % wc[word])
                else: self.file.write('\t0')
            self.file.write('\n')
        for d in self.articles:
            try:
                self.fileInfo.write(d)
            except:
                self.fileInfo.write('error')
            self.fileInfo.write('\n')
        self.file.close()
        self.fileInfo.close()

# Create the database tables
    def createindextables(self):
        print "Creating a file repertory for raw texts"
        os.rename("./src","./src_old")
        os.mkdir("./src")

        print "Creating SQL tables"
        self.con.execute('create table articleList(title,source,author,link,published,file)')
        self.con.execute('create table wordList(word,wordid integer primary key)')
        self.con.execute('create table wordCount(articleid,wordid,wcount)')

        self.con.execute('create index wordidx on wordList(word)')
        self.con.execute('create index articleidx on articleList(title)')
        self.con.execute('create index articlewordidx on wordCount(articleid)')
        self.con.execute('create index wordarticleidx on wordCount(wordid)')
        self.dbcommit()