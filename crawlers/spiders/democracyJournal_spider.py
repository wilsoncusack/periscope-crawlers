from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor

from crawlers.items import newsItem
import unicodedata

class nyt(CrawlSpider):
    name = "democracy"
    allowed_domains = ["democracyjournal.org"]
    start_urls = [
    "https://www.democracyjournal.org/",
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths=['//*[@id="content_left"]/h1/a']),callback='parse_item', follow=True),
        )

    def parse_item(self, response):
        try:
            sel = Selector(response)
            title = sel.xpath('//*[@id="content_article"]/h1/text()')
            author = sel.xpath('//*[@id="content_article"]/div[2]/text()')
            #content = sel.xpath('//*[@id="story"]/p[1]/text()') #List
            content = sel.xpath('//*[@id="content_article"]/p/text()')
            link = sel.xpath('/html/head/meta[5]/@content')
            description = sel.xpath('//*[@id="content_article"]/h2/text()')

            item = newsItem()

            try:
                date = sel.xpath('//*[@id="content_article"]/div[1]/text()').split(",")[1]
                item['date'] = unicodedata.normalize('NFKD', date[0].extract()).encode('ascii', 'ignore')
            except:
                item['date'] = -1

            item['title'] = unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            item['link'] = unicodedata.normalize('NFKD', link[0].extract()).encode('ascii', 'ignore')
            item['author'] = unicodedata.normalize('NFKD', author[0].extract()).encode('ascii', 'ignore')
            item['description'] = unicodedata.normalize('NFKD', description[0].extract()).encode('ascii', 'ignore')
            item['publication'] = 'Democracy Journal'
            item['politicalScore'] = -150
            item['posNegScore'] = 0
            wholeBody = ''
            for part in content:
                wholeBody += unicodedata.normalize('NFKD', part.extract()).encode('ascii', 'ignore')
            item['body'] = unicodedata.normalize('NFKD', content[0].extract()).encode('ascii', 'ignore')
            item['body'] = wholeBody

            return [item]
        except:
            print("res" + str(response))
            return []
