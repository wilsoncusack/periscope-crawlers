from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from crawlers.items import newsItem
import unicodedata

class WeeklyStandard(CrawlSpider):
    name = "weeklyStandard"
    allowed_domains = ["weeklystandard.com"]
    start_urls = ["http://www.weeklystandard.com/", "http://www.weeklystandard.com/politics-and-government", "http://www.weeklystandard.com/foreign-policy-and-national-security", "http://www.weeklystandard.com/books-arts-and-society", "http://www.weeklystandard.com/issue/current"]

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=['//*[@id="featured-teasers"]/div/div/h2/a','//*[@id="center"]/div/div/h2/a', '//*[@id="center"]/div/div/div[2]/h2/a', '//*[@id="center"]/div/div[1]/h2/a', '//*[@id="center"]/div/div/h2/a', '//*[@id="center"]/div/div/div/h2/a']),callback='parse_item', follow=True),
        )

    def parse_item(self, response):
        try:
            sel = Selector(response)
            #print response
            title = sel.xpath('//*[@id="center"]/div[2]/h1/text()')
            #print '           '
            #print unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            #print '           '
            #try:
            author = sel.xpath('//*[@id="center"]/div[2]/div[1]/span/a/text()')
            #    item['author'] = unicodedata.normalize('NFKD', author[0].extract()).encode('ascii', 'ignore')
            #except:
            #    item['author'] = ''
                
            #content = sel.xpath('//*[@id="story"]/p[1]/text()') #List
            content = sel.xpath('//*[@id="center"]/div[6]/div[1]/p/text()')
            link = sel.xpath('/html/head/meta[4]/@content')


            item = newsItem()

            try:
                date = sel.xpath('//*[@id="center"]/div[2]/div[1]/span/span/text()')
                item['date'] = unicodedata.normalize('NFKD', date[0].extract()).encode('ascii', 'ignore')
            except:
                item['date'] = -1


            item['title'] = unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            item['link'] = unicodedata.normalize('NFKD', link[0].extract()).encode('ascii', 'ignore')
            item['author'] = unicodedata.normalize('NFKD', author[0].extract()).encode('ascii', 'ignore')
            item['publication'] = 'The Weekly Standard'
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
