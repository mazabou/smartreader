import sqlite3 as sqlite

class ParseTodb:
    def __init__(self):
        dbname = "parseddata.db"
        print "Connecting to the database "+dbname
        self.con = sqlite.connect(dbname)
        self.createindextables()

    def add(self,title, source, author, url, published , words):
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

# Return true if this url is already indexed
    def isindexed(self,url):
        u = self.con.execute("select rowid from articleList where link='%s'" % url).fetchone()
        return (u != None)

    def commit(self):
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
            words_tuple = self.con.execute('select word,wordid from wordList').fetchall()
            words = [t[0] for t in words_tuple]
            wordids = {}
            for i in range(len(words)):
                wordids[words_tuple[i][1]]=i
            articles = [t[0] for t in self.con.execute('select title from articleList').fetchall()]
            data = self.con.execute('select articleid,wordid,wcount from wordCount').fetchall()
            #count = [[0]*len(words)]*len(articles)
            count = [[0]*len(words) for i in range(len(articles))]
            for t in data:
                count[t[0]-1][wordids[t[1]]]=t[2]
            return articles, words, count