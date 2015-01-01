from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from crawlers.items import newsItem
import unicodedata

class foreignAffairs(CrawlSpider):
    name = "foreignAffairs"
    allowed_domains = ["foreignaffairs.com"]
    start_urls = ["http://www.foreignaffairs.com/", "http://www.foreignaffairs.com/regions", "http://www.foreignaffairs.com/topics", "http://www.foreignaffairs.com/features"]

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=['//*[@id="content-area"]/div/div/div/div/div/div/div/h1/a', '//*[@id="content-area"]/div/div/div/div/div/div/div/div/h2/a', '//*[@id="content-area"]/div/div/div/div/div/div/div/table/tbody/tr/td/div/div/span/a', '//*[@id="regions"]/div/div/div/div/div/div/div/div/span/a']),callback='parse_item', follow=True), 
        )

    def parse_item(self, response):
        try:
            sel = Selector(response)
            #print response
            title = sel.xpath('//*[@id="content-header"]/div[2]/h1/text()') 
            #print '           '
            #print unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            #print '           '
            author = sel.xpath('//*[@id="content-header"]/div[3]/div[1]/a/text()')
            #content = sel.xpath('//*[@id="story"]/p[1]/text()') #List
            content = sel.xpath('//*[@id="content-main-area"]/div/div/div/div/p/text()') 
            link = sel.xpath('/html/head/link[3]/@href')


            item = newsItem()

            try:
                date = sel.xpath('//*[@id="content-header"]/div[3]/div[3]/span/text()')
                item['date'] = unicodedata.normalize('NFKD', date[0].extract()).encode('ascii', 'ignore')
            except:
                item['date'] = -1

            item['title'] = unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            item['link'] = unicodedata.normalize('NFKD', link[0].extract()).encode('ascii', 'ignore')
            item['author'] = unicodedata.normalize('NFKD', author[0].extract()).encode('ascii', 'ignore')
            item['publication'] = 'Foreign Affairs'
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
