from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from crawlers.items import newsItem
import unicodedata

class nyt(CrawlSpider):
    name = "nyt"
    allowed_domains = ["nytimes.com"]
    start_urls = [
    # "http://www.nytimes.com/", 
    "http://topics.nytimes.com/top/opinion/editorialsandoped/oped/columnists/index.html",
    "http://opinionator.blogs.nytimes.com/",
    "http://www.nytimes.com/pages/opinion/index.html?",
    #"http://topics.nytimes.com/top/opinion/editorialsandoped/editorials/index.html", 
    # "http://topics.nytimes.com/top/opinion/editorialsandoped/oped/contributors/index.html", 
    # "http://www.nytimes.com/pages/opinion/", "http://www.nytimes.com/pages/world/", 
    # "http://www.nytimes.com/pages/national/",  "http://www.nytimes.com/pages/nyregion/",  "http://www.nytimes.com/pages/business/",  "http://www.nytimes.com/pages/science/",  "http://www.nytimes.com/pages/fashion/"
    ]

    # rules = (
    #     Rule(SgmlLinkExtractor(restrict_xpaths=['//*[@class="post"]/header/h3/a','//*[@id="searchList"]/div/h4/a', '//*[@id="spanABTopRegion"]/div[1]/div/div/div/div/h3/a', '//*[@id="feedContent"]/div/h3/a', '//*[@id="main"]/div/div/div[1]/div[1]/div[1]/div/h3/a', '//*[@id="spanABCRegion"]/div[1]/div[2]/div/div[1]/h3/a', '//div[@class="story"]/h3/a','//div[@class="story"]/h4/a','//div[@class="story"]/h5/a']),callback='parse_item', follow=True),
    #     )

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=['//*[@id="spanABTopRegion"]/div/div/div/div/h2/a','//*[@id="spanABTopRegion"]/div[3]/div/div[2]/div/div/h3/a', '//*[@id="searchList"]/div/h4/a', '//*[@class="post"]/header/h3/a', '//*[@id="spanABCRegion"]/div[1]/div[2]/div/div/h3/a']),callback='parse_item', follow=True),
        )


    def parse_item(self, response):
        try:
            sel = Selector(response)
            try:
                title = sel.xpath('//*[@id="story-heading"]/text()')
                # author = sel.xpath('//*[@id="story-header"]/div/div/p/span/a/span/text()')
                author = sel.xpath('//*[@class="byline-author"]/text()')
            except:
                # opinionator
                title = sel.xpath('[@class="entry-title"]/text()')
                author = sel.xpath('//*[@class="post"]/header/div[2]/address/a/address/span/text()')

            #print '           '
            #print unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            #print '           '
            
            
            #content = sel.xpath('//*[@id="story"]/p[1]/text()') #List
            content = sel.xpath('//*[@class="story-body-text story-content"]/text()')
            link = sel.xpath('/html/head/link[5]/@href')



            item = newsItem()

            try:
                date = sel.xpath('//*[@id="story-header"]/div/div/p/time/text()')
                item['date'] = unicodedata.normalize('NFKD', date[0].extract()).encode('ascii', 'ignore')
            except:
                item['date'] = -1
            
            item['title'] = unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore').split("The New York Times")[0]
            item['link'] = unicodedata.normalize('NFKD', link[0].extract()).encode('ascii', 'ignore')
            item['author'] = unicodedata.normalize('NFKD', author[0].extract()).encode('ascii', 'ignore')
            item['publication'] = 'The New York Times'
            item['politicalScore'] = -100
            item['posNegScore'] = 0
            wholeBody = ''
            for part in content:
                wholeBody += unicodedata.normalize('NFKD', part.extract()).encode('ascii', 'ignore')
            item['body'] = unicodedata.normalize('NFKD', content[0].extract()).encode('ascii', 'ignore')
            item['body'] = wholeBody
            

            # print item['title'] + item['author'] + item['link'] 
            # print item['body']


            return [item]
        except:
            print("res" + str(response))
            return []
