from notebooks.scrapy import Spider12
from scrapy.crawler import CrawlerProcess

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(Spider12)
    process.start()
