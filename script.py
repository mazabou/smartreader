import crawl
scraper = crawl.scraper("firstdb.db")
scraper.createindextables() #execute the first time
scraper.setFeedList("rssList.txt")
scraper.scrap()
