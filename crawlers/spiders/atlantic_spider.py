from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from crawlers.items import newsItem
import unicodedata

class atlantic(CrawlSpider):
    name = "atlantic"
    allowed_domains = ["theatlantic.com"]
    start_urls = ["http://www.theatlantic.com/","http://www.theatlantic.com/politics/","http://www.theatlantic.com/business/","http://www.theatlantic.com/technology/","http://www.theatlantic.com/entertainment/","http://www.theatlantic.com/health/","http://www.theatlantic.com/education/","http://www.theatlantic.com/sexes/","http://www.theatlantic.com/national/","http://www.theatlantic.com/international/"]

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=['//*[@id="homepage-btf"]/div/ul/li/article/a', '//*[@id="carousel"]/nav/a', '//*[@id="homepage-btf"]/ul/li/article/a', '//*[@id="container"]/div/div/div/ul/li/h3', '//*[@id="container"]/div/div/div/div/h3/a', '//*[@id="container"]/div/div/ul/li/div/h3/a']),callback='parse_item', follow=True),
        )
    # //*[@id="container"]/div[2]/div[1]/div[2]/ul/li[1]/h3
    # //*[@id="container"]/div[2]/div[1]/div[2]/div/h3/a
    # //*[@id="container"]/div[2]/div[1]/div[2]/ul/li[1]/h3/a
    # //*[@id="container"]/div[2]/div[1]/ul/li[14]/div/h3/a
    
    # //*[@id="homepage-btf"]/div/ul/li[2]/article/a
    # //*[@id="homepage-btf"]/div/ul/li[3]/article/a[1]
    # //*[@id="carousel"]/nav/a[3]
    # //*[@id="homepage-btf"]/ul/li[2]/article/a


    def parse_item(self, response):
        try:
            sel = Selector(response)
            #print response
            title = sel.xpath('//*[@id="article"]/h1/text()')
            #print '           '
            #print unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            #print '           '
            author = sel.xpath('//*[@id="article"]/div[2]/span[1]/a/text()')
            #content = sel.xpath('//*[@id="story"]/p[1]/text()') #List
            content = sel.xpath('//*[@id="article"]/div[5]/p/text()')
            link = sel.xpath('/html/head/link[9]/@href')


            item = newsItem()

            item['title'] = unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            item['link'] = unicodedata.normalize('NFKD', link[0].extract()).encode('ascii', 'ignore')
            item['author'] = unicodedata.normalize('NFKD', author[0].extract()).encode('ascii', 'ignore')
            item['publication'] = 'Atlantic'
            item['politicalScore'] = 0
            item['posNegScore'] = 0
            # need date
            wholeBody = ''
            for part in content:
                wholeBody += unicodedata.normalize('NFKD', part.extract()).encode('ascii', 'ignore')
            item['body'] = unicodedata.normalize('NFKD', content[0].extract()).encode('ascii', 'ignore')
            item['body'] = wholeBody
            #print(link)

            return [item]
        except:
            return []


