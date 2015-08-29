from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor

from crawlers.items import newsItem
import unicodedata

class NPR(CrawlSpider):
    name = "NPR"
    allowed_domains = ["npr.org"]
    start_urls = ["http://www.npr.org/sections/news/", "http://www.npr.org/sections/us/", "http://www.npr.org/sections/world/", "http://www.npr.org/sections/politics/", "http://www.npr.org/sections/business/", "http://www.npr.org/sections/technology/", "http://www.npr.org/sections/science/", "http://www.npr.org/sections/health/"]

    rules = (
        Rule(LinkExtractor(restrict_xpaths=['//*[@id="featured"]/div/article/div[2]/h1/a', '//*[@id="overflow"]/article/div[2]/h1/a']),callback='parse_item', follow=True),
        )

    def parse_item(self, response):
        try:
            sel = Selector(response)
            #print response
            title = sel.xpath('//*[@id="sectionWrap"]/section/article/div[1]/h1/text()')
            #print '           '
            #print unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            #print '           '
            #try:
            author = sel.xpath('//*[@id="storybyline"]/div/div/div/div/a/div/div/text()')
            #    item['author'] = unicodedata.normalize('NFKD', author[0].extract()).encode('ascii', 'ignore')
            #except:
            #    item['author'] = ''
                
            #content = sel.xpath('//*[@id="story"]/p[1]/text()') #List
            content = sel.xpath('//*[@id="storytext"]/p/text()')
            link = sel.xpath('/html/head/link[1]/@href')


            item = newsItem()

            try:
                date = sel.xpath('//*[@id="story-meta"]/div[1]/time/span[1]/text()')
                item['date'] = unicodedata.normalize('NFKD', date[0].extract()).encode('ascii', 'ignore')
            except:
                item['date'] = -1


            item['title'] = unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            item['link'] = unicodedata.normalize('NFKD', link[0].extract()).encode('ascii', 'ignore')
            item['author'] = unicodedata.normalize('NFKD', author[0].extract()).encode('ascii', 'ignore')
            item['publication'] = 'NPR'
            item['politicalScore'] = -2
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
