import urllib2
import feedparser
from bs4 import BeautifulSoup
import sqlite3 as sqlite
import re

# Create a list of words to ignore
ignorewords=set(['the','of','to','and','a','in','is','it'])

class scraper:
# Initialize the crawler with the name of database
    def __init__(self,dbname):
        self.con = sqlite.connect(dbname)

    def __del__(self):
        self.con.close()

    def dbcommit(self):
        self.con.commit()

    def scrap(self,rssFeed):
        rss = feedparser.parse(rssFeed)
        for entry in rss.entries:
            title = entry["title"]
            author = entry["author"]
            published = entry["published_parsed"]
            url = entry["link"]
            try:
                c = urllib2.urlopen(url)
            except:
                print "Could not open %s" % url
                continue
            soup = BeautifulSoup(c.read(),"html.parser")
            self.addtoindex(url, soup, title, author, published)
            self.dbcommit()

            # Index an individual page
    def addtoindex(self, url, soup, title, author, published):
            if self.isindexed(url): return
            print 'Indexing ' + url
            # Get the individual words
            text = self.getArticle(soup)
            text = text.encode('utf-8')

            filename = './src/'+title + '.txt'
            file = open(filename,'w')
            file.write(text)
            file.close()

            words = self.separatewords(text)

            # Get the URL id
            cur = self.con.execute("insert into articleList (title,source,author,link,published,file) values ('%s', '%s', '%s', '%s', '%s', '%s')" % (title, 'NYT', author, published, url, filename))
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
    def getArticle(self, soup):
        matches = soup.findAll("p", {"class": "story-body-text story-content"})
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
        splitter = re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s != '']

# Return true if this url is already indexed
    def isindexed(self,url):
        u = self.con.execute("select rowid from articleList where link='%s'" % url).fetchone()
        return (u != None)
            
# Create the database tables
    def createindextables(self):
        self.con.execute('create table articleList(title,source,author,link,published,file)')
        self.con.execute('create table wordList(word)')
        self.con.execute('create table wordCount(articleid,wordid,wcount)')

        self.con.execute('create index wordidx on wordList(word)')
        self.con.execute('create index articleidx on articleList(title)')
        self.con.execute('create index articlewordidx on wordCount(articleid)')
        self.con.execute('create index wordarticleidx on wordCount(wordid)')
        self.dbcommit()