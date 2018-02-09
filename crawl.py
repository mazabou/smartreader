import urllib2
from bs4 import BeautifulSoup
c = urllib2.urlopen("https://www.nytimes.com/2018/02/09/world/asia/olympics-opening-ceremony-north-korea.html?rref=collection%2Fsectioncollection%2Fworld&action=click&contentCollection=world&region=rank&module=package&version=highlights&contentPlacement=1&pgtype=sectionfront")
soup=BeautifulSoup(c.read(),"html.parser")
matches = soup.findAll("p", {"class":"story-body-text story-content"})
for m in matches:
	print m.contents