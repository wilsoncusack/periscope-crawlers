from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from crawlers.items import newsItem
import unicodedata

class NewRepublic(CrawlSpider):
    name = "newRepublic"
    allowed_domains = ["newrepublic.com"]
    start_urls = ["http://www.newrepublic.com/", "http://www.newrepublic.com/tags/politics", "http://www.newrepublic.com/tags/culture", "http://www.newrepublic.com/latest"]

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=['//*[@id="homepage"]/div/div/div/div/div/div/h3/a', '//*[@id="homepage"]/div/div/div/div/div/h3/a', '//*[@id="homepage"]/div/div/div/div/h2/a', '//*[@id="tag"]/div/div/div/div/div/div/div[2]/h3/a', '//*[@id="latest"]/div/div/div/div/div/div/div[2]/h3/a']),callback='parse_item', follow=True),
        )

    def parse_item(self, response):
        try:
            sel = Selector(response)
            #print response
            title = sel.xpath('//*[@id="article"]/div[2]/div[1]/div[2]/div[1]/div/h1/span/text()')
            #print '           '
            #print unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            #print '           '
            #try:
            author = sel.xpath('//*[@id="article"]/div[2]/div[1]/div[2]/div[2]/div/div[2]/div[1]/h5/a/text()')
            #    item['author'] = unicodedata.normalize('NFKD', author[0].extract()).encode('ascii', 'ignore')
            #except:
            #    item['author'] = ''
                
            #content = sel.xpath('//*[@id="story"]/p[1]/text()') #List
            content = sel.xpath('//*[@id="article"]/div[2]/div[1]/div[2]/div[2]/div/div[2]/div[1]/div/p/text()')
            link = sel.xpath('/html/head/link[6]/@href')


            item = newsItem()

            try:
                date = sel.xpath('//*[@id="article"]/div[2]/div[1]/div[2]/div[1]/div/h5/span/text()')
                item['date'] = unicodedata.normalize('NFKD', date[0].extract()).encode('ascii', 'ignore')
            except:
                item['date'] = -1


            item['title'] = unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            item['link'] = unicodedata.normalize('NFKD', link[0].extract()).encode('ascii', 'ignore')
            item['author'] = unicodedata.normalize('NFKD', author[0].extract()).encode('ascii', 'ignore')
            item['publication'] = 'New Republic'
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
