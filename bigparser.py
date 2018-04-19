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

        # Pulling the data from the rss file
        #self.rssList = ["articles1.csv","articles2.csv","articles3.csv"]
        self.rssList = ["articles1.csv"]
        self.saveArticles = saveArticles


    def parse(self):
        for fichier in self.rssList:
            df = pd.read_csv(fichier)
            for index, row in df.iterrows():
                self.addtoindex(str(row['url']), row['content'], str(row['title']).decode('utf-8'), str(row['publication']).decode('utf-8'), 'News', str(row['author']).decode('utf-8'), str(row['date']))

    def commit(self,dataFilename='bigdata.csv',infoFilename='bigmetadata.csv'):
        self.out.commit(dataFilename,infoFilename)
        print 'The parsed articles have been successfully saved in data.csv, metadata.csv and words.csv'

    # Index an individual page
    def addtoindex(self, url, text, title, source, category, author, published):
            # Get the individual words
            #text = text.encode('utf-8') #probleme d'encodage rencontre
            words = self.separatewords(text)
            if words == []: return
            #stemmer = snowballstemmer.stemmer('english');
            #words = stemmer.stemWords(words)   
            self.out.add(title, source, category, author, url, published, words)

# Separate the words by any non-whitespace character
    def separatewords(self,text):
        splitter = re.compile(r'\W*')
        return self.filter([s.lower() for s in splitter.split(text) if s != ''])
    
    def filter(self,words):
        return [word for word in words if (len(word)>1 and word.isalpha() and word not in ignorewords)] #list comprehension