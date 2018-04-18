import urllib2
import feedparser
from bs4 import BeautifulSoup, Comment
import re
import os
import snowballstemmer
import pandas as pd
import time
import shutil

from ParseTotxt import ParseTotxt
from ParseTodb import ParseTodb

# Create a list of words to ignore
ignorewords=set(['the','of','to','and','a','in','is','it','an','by','from','with'])
tag_pattern = [("div", {"id": "story-body"}),("div", {"class": "article-body"}),("span", {"class": "entry-content"}),("div", {"itemprop": "articleBody"}),("div", {"property": "articleBody"}),("div", {"class": "news-content"}),("div", {"class": "post-content"}),("div", {"class": "entry"}),("div", {"class": "article-main-body"}),("div", {"class": "ctx_content"}),("div", {"class": "blog-post__text"}),("div", {"class": "js-content-entity-body"}),("article", {"class": "main-copy"}),("div", {"class": "paragraphs"}),("div", {"class": "articleText"}),("div", {"class": "storytext"}),("div", {"id": "articleBody"}),("div", {"class": "article-text"}),("div", {"class": "story-text"}),("div", {"class": "body_1gnLA"}),("div", {"class": "body"}),("section", {"class": "article-body"}),("div", {"class": "content"}),("article", {"class": "c-content"})]

class Parser:
    def __init__(self,out="txt",rssFile="rssList.csv",quickCheck=False,saveArticles=False):
        # Set up the output
        if out == "txt":
            self.out = ParseTotxt()
        elif out == "db":
            self.out = ParseTodb()

        if quickCheck:
            print 'Warning: This will only be parsing one RSS feed for testing purposes //Doesnt work'
            #self.rssList=pd.DataFrame({"NYT":"http://www.nytimes.com/services/xml/rss/nyt/HomePage.xml"}
        else:
            # Pulling the data from the rss file
            self.rssList = {}
            print "Pulling the RSS Feeds list from " + rssFile + "..."
            self.setFeedList(rssFile)

        self.saveArticles = saveArticles
        if saveArticles:
            print "Preparing the file repertory for raw texts..."
            try:
                os.rename("./src","./src_old")
                os.mkdir("./src")
            except:
                print 'Error with /scr'

    def setFeedList(self,filename):
       self.rssList = pd.read_csv('rssList.csv')

    def parse(self):
        self.detectederrors = []
        self.times = []
        for index,source,category,feed in self.rssList.itertuples():
            rss = feedparser.parse(feed)

            print "Connecting to " + source
            print "-----------------------------------------------"

            NoErrorDetected = True
            for entry in rss.entries:
                start = time.time()
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
                if "picture" in url: continue
                try:
                    c = urllib2.urlopen(url)
                except:
                    print "Could not open %s" % url
                    NoErrorDetected = False
                    continue
                soup = BeautifulSoup(c.read(),"html.parser")
                self.addtoindex(url, soup, title, source, category, author, published)
                stop = time.time()
                self.times.append(stop-start)
            if not NoErrorDetected: self.detectederrors.append(source)

        print "Parsing Over. Don't forget to commit!"

    def info(self):
        print 'Average parsing time per article: ' + str(sum(self.times)/float(len(self.times)))
        print 'There are problems with: ' + ','.join(self.detectederrors)


    def commit(self,dataFilename='data.csv',infoFilename='metadata.csv'):
        self.out.commit(dataFilename,infoFilename)
        print 'The parsed articles have been successfully saved in data.csv, metadata.csv and words.csv'

    # Index an individual page
    def addtoindex(self, url, soup, title, source, category, author, published):
            if self.out.isindexed(title): return
            if title == '': return

            print ' Indexing ' + url

            # Get the individual words
            text = self.getArticle(soup)
            text = text.encode('utf-8') #probleme d'encodage rencontre
            if len(text)<2000: return

            if self.saveArticles: self.save(text,title,url)

            words = self.separatewords(text)

            #stemmer = snowballstemmer.stemmer('english');
            #words = stemmer.stemWords(words)
            if len(words) <> 0:
                self.out.add(title, source, category, author, url, published, words)
        

# Extract the text from an HTML page (no tags)
    def getArticle(self,soup):
        matchfound = False
        for t in tag_pattern:
            match = soup.find(t[0],t[1])
            if match != None:
                matchfound = True
                break
        if not matchfound:
            match = soup
        for element in match(text=lambda text: isinstance(text, Comment)):
            element.extract()
        for i in match.find_all(["i","aside","script"]): 
            i.decompose()
        matches = match.findAll("p")
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

    def save(self,text,title,url):
        s = title.encode('ascii','ignore')
        s = str(s).strip().replace(' ', '_')
        filename = re.sub(r'(?u)[^-\w.]', '', s)
        #filename = title.encode('ascii','ignore')
        
        filename = './src/'+ filename + '.txt'
        try:
            file = open(filename,'w')
            file.write(url+'\n')
            file.write(text)
            file.close()
        except:
            print "Error, filename = "+ filename

# Separate the words by any non-whitespace character
    def separatewords(self,text):
        splitter = re.compile(r'\W*')
        return self.filter([s.lower() for s in splitter.split(text) if s != ''])
    
    def filter(self,words):
        return [word for word in words if (len(word)>1 and word.isalpha() and word not in ignorewords)] #list comprehension