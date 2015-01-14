from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from crawlers.items import newsItem
import unicodedata

class nyt(CrawlSpider):
    name = "nyt"
    allowed_domains = ["nytimes.com"]
    start_urls = ["http://www.nytimes.com/", "http://www.nytimes.com/pages/world/", "http://www.nytimes.com/pages/national/",  "http://www.nytimes.com/pages/nyregion/",  "http://www.nytimes.com/pages/business/",  "http://www.nytimes.com/pages/science/",  "http://www.nytimes.com/pages/fashion/"]

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=['//div[@class="story"]/h3/a','//div[@class="story"]/h4/a','//div[@class="story"]/h5/a']),callback='parse_item', follow=True),
        ) 

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
            link = sel.xpath('/html/head/link[5]/@href')


            item = newsItem()

            try:
                date = sel.xpath('//*[@id="story-header"]/div/div/p/time/text()')
                item['date'] = unicodedata.normalize('NFKD', date[0].extract()).encode('ascii', 'ignore')
            except:
                item['date'] = -1

            item['title'] = unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            item['link'] = unicodedata.normalize('NFKD', link[0].extract()).encode('ascii', 'ignore')
            item['author'] = unicodedata.normalize('NFKD', author[0].extract()).encode('ascii', 'ignore')
            item['publication'] = 'The New York Times'
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
