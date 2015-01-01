from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from crawlers.items import newsItem
import unicodedata

class economist(CrawlSpider):
    name = "economist"
    allowed_domains = ["economist.com"]
    start_urls = ["https://www.economist.com/", "https://www.economist.com/news/world-week/21600185-politics-week", "https://www.economist.com/business-finance", "https://www.economist.com/economics", "https://www.economist.com/science-technology", "https://www.economist.com/culture"]

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=['//*[@id="hero"]/li/div/a', '//*[@id="homepage-center-inner"]/section/article/a', '//*[@id="homepage-highlight-1"]/article/a', '']),callback='parse_item', follow=True),
        )
    # 

    def parse_item(self, response):
        try:
            sel = Selector(response)
            #print response
            title = sel.xpath('/html/head/title/text()')
            #print '           '
            #print unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            #print '           '
            author = sel.xpath('//*[@id="story-header"]/div/div/p/span/a/span/text()')
            #content = sel.xpath('//*[@id="story"]/p[1]/text()') #List
            content = sel.xpath('//*[@class="story-body-text story-content"]/text()')
            link = sel.xpath('/html/head/link[2]/@href')


            item = newsItem()

            try:
                date = sel.xpath('//*[@id="story-header"]/div/div/p/time/text()')
                item['date'] = unicodedata.normalize('NFKD', date[0].extract()).encode('ascii', 'ignore')
            except:
                item['date'] = -1

            item['title'] = unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            item['link'] = unicodedata.normalize('NFKD', link[0].extract()).encode('ascii', 'ignore')
            item['author'] = unicodedata.normalize('NFKD', author[0].extract()).encode('ascii', 'ignore')
            item['publication'] = 'Economist'
            item['politicalScore'] = 0
            item['posNegScore'] = 0

            wholeBody = ''
            for part in content:
                wholeBody += unicodedata.normalize('NFKD', part.extract()).encode('ascii', 'ignore')
            item['body'] = unicodedata.normalize('NFKD', content[0].extract()).encode('ascii', 'ignore')
            item['body'] = wholeBody
            #print(link)

            return [item]
        except:
            return []
