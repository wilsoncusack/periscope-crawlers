from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from crawlers.items import newsItem
import unicodedata

class Guardian(CrawlSpider):
    name = "Guardian"
    allowed_domains = ["theguardian.com"]
    start_urls = ["http://www.theguardian.com/", "http://www.theguardian.com/us-news", "http://www.theguardian.com/world", "http://www.theguardian.com/us/business"]

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=['//*[@id="us-news"]/div/div/div/ul/li/div/div/a', '//*[@id="us-news"]/div/div/div/ul/li/ul/li/div/div/a', '//*[@id="us-politics"]/div/div/div/ul/li/div/div/a', '//*[@id="us-politics"]/div/div/div/ul/li/ul/li/div/div/a', '//*[@id="opinion-&-analysis"]/div/div/div/ul/li/div/div/a', '//*[@id="opinion-&-analysis"]/div/div/div/ul/li[3]/ul/li/div/div/a', '//*[@id="world-news"]/div/div/div/ul/li/div/div/a', '//*[@id="world-news"]/div/div/div/ul/li/ul/li/div/div/a', '//*[@id="world-networks"]/div/div/div/ul/li/div/div/a[2]', '//*[@id="world-networks"]/div/div/div/ul/li/ul/li/div/div/a[2]', '//*[@id="around-the-world"]/div/div/div/ul/li/div/div/a[2]', '//*[@id="around-the-world"]/div/div/div/ul/li[3]/ul/li/div/div/a[2]', '//*[@id="in-case-you-missed"]/div/div/div/ul/li/div/div/a', '//*[@id="business"]/div/div/div/ul/li/div/div/a', '//*[@id="business"]/div/div/div/ul/li[3]/ul/li/div/div/a']),callback='parse_item', follow=True),
        )

    def parse_item(self, response):
        try:
            sel = Selector(response)
            #print response
            title = sel.xpath('//*[@id="article"]/header/div[1]/div/div/h1//text()')
            #print '           '
            #print unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            #print '           '
            #try:
            author = sel.xpath('//*[@id="article"]/div/div/div[1]/div[2]/p[1]/span/a/text()')
            #    item['author'] = unicodedata.normalize('NFKD', author[0].extract()).encode('ascii', 'ignore')
            #except:
            #    item['author'] = ''
                
            #content = sel.xpath('//*[@id="story"]/p[1]/text()') #List
            content = sel.xpath('//*[@id="article"]/div/div/div[1]/div[3]/p/text()')
            link = sel.xpath('//*[@id="js-context"]/head/link[15]/@href')


            item = newsItem()

            try:
                date = sel.xpath('//*[@id="article"]/div/div/div[1]/div[2]/p[2]/time/text()')
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
