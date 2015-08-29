from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor

from crawlers.items import newsItem
import unicodedata

class nyt(CrawlSpider):
    name = "jacobin"
    allowed_domains = ["jacobinmag.com"]
    start_urls = [
    "https://www.jacobinmag.com/category/blogs", 
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths=['//header/div/h3/a']),callback='parse_item', follow=True),
        )

    def parse_item(self, response):
        try:
            sel = Selector(response)
            #print response
            title = sel.xpath('//header/h2/a/text()')
            #print '           '
            #print unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            #print '           '
            author = sel.xpath('//header/div/a/text()')
            #content = sel.xpath('//*[@id="story"]/p[1]/text()') #List
            content = sel.xpath('//div/p/text()')
            link = sel.xpath('//header/h2/a/@href')

            item = newsItem()

            try:
                # Not sure why this isn't working
                description = sel.xpath('//*[@class="entry-dek"]/p/text()')
                item['description'] = unicodedata.normalize('NFKD', description[0].extract()).encode('ascii', 'ignore')
            except: 
                item['description'] = ''

            try:
                date = sel.xpath('//*[@id="top-side"]/div[1]/div[2]/text()')
                item['date'] = unicodedata.normalize('NFKD', date[0].extract()).encode('ascii', 'ignore')
            except:
                item['date'] = -1

            item['title'] = unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            item['link'] = unicodedata.normalize('NFKD', link[0].extract()).encode('ascii', 'ignore')
            item['author'] = unicodedata.normalize('NFKD', author[0].extract()).encode('ascii', 'ignore')
            item['publication'] = 'Jacobin'
            item['politicalScore'] = -200
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
