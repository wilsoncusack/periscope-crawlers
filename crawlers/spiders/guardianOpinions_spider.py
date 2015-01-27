from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from crawlers.items import newsItem
import unicodedata

class GuardianOpinion(CrawlSpider):
    name = "GuardianOpinion"
    allowed_domains = ["theguardian.com"]
    start_urls = ["http://www.theguardian.com/us/commentisfree"]

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=['//*[@id="opinion"]/div/div/div/ul/li/ul/li/div/div/a', '//*[@id="talking-points"]/div/div/div/ul/li/div/div/a', '//*[@id="talking-points"]/div/div/div/ul/li/ul/li/div/div/a', '//*[@id="in-case-you-missed"]/div/div/div/ul/li/div/div/a']),callback='parse_item', follow=True),
        )

    def parse_item(self, response):
        try:
            sel = Selector(response)
            #print response
            title = sel.xpath('//*[@id="article"]/header/div[1]/div/div/h1/text()')
            #print '           '
            #print unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            #print '           '
            #try:
            author = sel.xpath('//*[@id="article"]/header/div[1]/div/div/span/span/a/text()')
            #    item['author'] = unicodedata.normalize('NFKD', author[0].extract()).encode('ascii', 'ignore')
            #except:
            #    item['author'] = ''
                
            #content = sel.xpath('//*[@id="story"]/p[1]/text()') #List
            content = sel.xpath('//*[@id="article"]/div/div/div[1]/div[3]/p/text()')
            link = sel.xpath('//*[@id="js-context"]/head/link[15]/@href')


            item = newsItem()

            try:
                date = sel.xpath('//*[@id="article"]/div/div/div[1]/div[2]/p/time/text()')
                item['date'] = unicodedata.normalize('NFKD', date[0].extract()).encode('ascii', 'ignore')
            except:
                item['date'] = -1


            item['title'] = unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            item['link'] = unicodedata.normalize('NFKD', link[0].extract()).encode('ascii', 'ignore')
            item['author'] = unicodedata.normalize('NFKD', author[0].extract()).encode('ascii', 'ignore')
            item['publication'] = 'The Guardian'
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
