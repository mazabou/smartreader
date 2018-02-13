import urllib2
from bs4 import BeautifulSoup
c = urllib2.urlopen("https://www.cnbc.com/2018/02/12/opec-chief-says-he-has-putins-word-russia-wont-flood-market-with-oil.html")
soup=BeautifulSoup(c.read(),"html.parser")
matches = soup.findAll("p")
for m in matches:
	print m.contents