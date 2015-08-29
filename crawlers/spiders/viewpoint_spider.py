from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor


from crawlers.items import newsItem
import unicodedata
import datetime

class nyt(CrawlSpider):
    now = datetime.datetime.now()
    name = "viewpoint"
    allowed_domains = ["viewpointmag.com"]
    start_urls = [
    "https://viewpointmag.com/",
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths=['//header/h2/a', '//*[@class="post-title"]/a']),callback='parse_item', follow=True),
        )

    def parse_item(self, response):
        try:
            sel = Selector(response)
            title = sel.xpath('//header/h1/a/text()')
            author = sel.xpath('//*[@class="byline"]/a/text()')
            #content = sel.xpath('//*[@id="story"]/p[1]/text()') #List
            content = sel.xpath('//*[@class="pf-content"]/p/text()')
            link = sel.xpath('//header/h1/a/@href')

            item = newsItem()

            try:
                date = sel.xpath('//*[@class="byline"]/time/@datetime')
                item['date'] = unicodedata.normalize('NFKD', date[0].extract()).encode('ascii', 'ignore')
            except:
                item['date'] = -1

            item['title'] = unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            item['link'] = unicodedata.normalize('NFKD', link[0].extract()).encode('ascii', 'ignore')
            item['author'] = unicodedata.normalize('NFKD', author[0].extract()).encode('ascii', 'ignore')
            item['publication'] = 'Viewpoint Magazine'
            item['politicalScore'] = -210
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
