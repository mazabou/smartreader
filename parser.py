import urllib2
import feedparser
from bs4 import BeautifulSoup
import sqlite3 as sqlite
import re
import os

from ParseTotxt import ParseTotxt

# Create a list of words to ignore
ignorewords=set(['the','of','to','and','a','in','is','it'])

class Parser:
    def __init__(self,out="txt",rssFile="rssList.txt",quickCheck=False):
        # Set up the output
        if out == "txt":
            self.out = ParseTotxt()
        if quickCheck:
            print 'Warning: This will only be parsing one RSS feed for testing purposes'
            self.rssList={"NYT":"http://www.nytimes.com/services/xml/rss/nyt/HomePage.xml"}
        else:
            # Pulling the data from the rss file
            self.rssList = {} 
            print "Pulling the RSS Feeds list from " + rssFile
            self.setFeedList(rssFile)


    def initDB(self,filename):
        print "Connecting to the database "+dbname
        self.con = sqlite.connect(dbname)
        if self.new:
            self.createindextables()


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
        self.out.commit()

    # Index an individual page
    def addtoindex(self, url, soup, title, source, author, published):
            if self.out.isindexed(url): return
            print 'Indexing ' + url
            # Get the individual words
            if source[:2] == "NYT":
                text = self.getArticleNYT(soup)
            else:
                text = self.getArticleP(soup)
            text = text.encode('utf-8') #probleme d'encodage rencontre
            words = self.separatewords(text)
            self.out.add(title, source, author, url, published, words)
            

    def addToDB(self,title, source, author, url, published , words):
            # Get the URL id
            cur = self.con.execute("insert into articleList (title,source,author,link,published,file) values (?, ?, ?, ?, ?, ?)", (title, source, author, url, published))
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

    def commitDB(self):
        self.con.commit()

# Create the database tables
    def createindextables(self):
        print "Creating SQL tables"
        self.con.execute('create table articleList(title,source,author,link,published,file)')
        self.con.execute('create table wordList(word,wordid integer primary key)')
        self.con.execute('create table wordCount(articleid,wordid,wcount)')

        self.con.execute('create index wordidx on wordList(word)')
        self.con.execute('create index articleidx on articleList(title)')
        self.con.execute('create index articlewordidx on wordCount(articleid)')
        self.con.execute('create index wordarticleidx on wordCount(wordid)')
        self.dbcommit()

    def readfile(self):
        return self.out.readfile()