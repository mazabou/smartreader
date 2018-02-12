import project
scraper = project.scraper("firstdb.db")
# scraper.createindextables() #execute the first time
scraper.scrap("http://www.nytimes.com/services/xml/rss/nyt/HomePage.xml")
