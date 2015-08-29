from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor

from crawlers.items import newsItem
import unicodedata
import datetime

class nyt(CrawlSpider):
    now = datetime.datetime.now()
    name = "federalist"
    allowed_domains = ["thefederalist.com"]
    start_urls = [
    "http://thefederalist.com/blog/",
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths=['//article/div/header/h2/a']),callback='parse_item', follow=True),
        )

    def parse_item(self, response):
        try:
            sel = Selector(response)
            #print response
            title = sel.xpath('//article/div[1]/div[4]/header/h2/a/text()')
            #print '           '
            #print unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            #print '           '
            author = sel.xpath('//article/div[1]/div[4]/div[4]/a/text()')
            #content = sel.xpath('//*[@id="story"]/p[1]/text()') #List
            content = sel.xpath('//div/p/text()')
            link = sel.xpath('//article/div[1]/div[4]/header/h2/a/@href')


            item = newsItem()

            try:
                date = sel.xpath('//article/div[1]/div[4]/div[4]/text()')
                print "---------" + date + "---------\n\n\n" 
                item['date'] = unicodedata.normalize('NFKD', date[0].extract()).encode('ascii', 'ignore')
            except:
                item['date'] = -1

            item['title'] = unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            item['link'] = unicodedata.normalize('NFKD', link[0].extract()).encode('ascii', 'ignore')
            item['author'] = unicodedata.normalize('NFKD', author[0].extract()).encode('ascii', 'ignore')
            item['publication'] = 'The Federalist'
            item['politicalScore'] = 200
            item['posNegScore'] = 0
            wholeBody = ''
            for part in content:
                wholeBody += unicodedata.normalize('NFKD', part.extract()).encode('ascii', 'ignore')
            item['body'] = unicodedata.normalize('NFKD', content[0].extract()).encode('ascii', 'ignore')
            item['body'] = wholeBody
            #print(link)

            return [item]
        except:
            print("res" + str(response))
            return []
