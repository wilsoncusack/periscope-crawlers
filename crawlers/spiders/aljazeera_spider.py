from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor

from crawlers.items import newsItem
import unicodedata

class Aljazeera(CrawlSpider):
    name = "Aljazeera"
    allowed_domains = ["america.aljazeera.com/", "aljazeera.com"]
    start_urls = ["http://america.aljazeera.com/opinions.html" 
    # "http://america.aljazeera.com/", 
    # "http://america.aljazeera.com/topics/topic/categories/us.html", 
    # "http://america.aljazeera.com/topics/topic/categories/international.html", 
    # "http://america.aljazeera.com/topics/topic/categories/economy.html", 
    # "http://america.aljazeera.com/topics/topic/categories/technology.html", 
    # "http://america.aljazeera.com/topics/topic/categories/science.html", 
    # "http://america.aljazeera.com/topics/topic/categories/environment.html", 
    # "http://america.aljazeera.com/topics/topic/categories/sports.html", 
    # "http://america.aljazeera.com/topics/topic/categories/culture.html", 
    # "http://america.aljazeera.com/topics/topic/issue/human-rights.html"
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths=[
            '/html/body/div[2]/div/div/div[1]/div/div/div/div/div[2]/div[2]/h3/a', '//*[@id="articleHighlightList-0"]/div/div/div[2]/article/div[2]/h3/a']),callback='parse_item', follow=True),
        )
# /html/body/div[2]/div/div/div[1]/div/div[3]/div/div/div[2]/div[2]/h3/a
# /html/body/div[2]/div/div/div[1]/div/div[3]/div/div/div[2]/div[1]/h3/a
# /html/body/div[2]/div/div/div[1]/div/div[4]/div/div/div[2]/div[1]/h3/a
# //*[@id="articleHighlightList-0"]/div/div/div[2]/article[1]/div[2]/h3/a
# //*[@id="articleHighlightList-0"]/div/div/div[2]/article[4]/div[2]/h3/a
    def parse_item(self, response):
        try:
            sel = Selector(response)
            #print response
            title = sel.xpath('/html/body/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div[3]/div/h1/text()')
            #print '           '
            #print unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            #print '           '
            #try:
            author = sel.xpath('/html/body/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div[4]/div/div[2]/span/a/text()')
            #    item['author'] = unicodedata.normalize('NFKD', author[0].extract()).encode('ascii', 'ignore')
            #except:
            #    item['author'] = ''
                
            #content = sel.xpath('//*[@id="story"]/p[1]/text()') #List
            content = sel.xpath('/html/body/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/p/text()')
            link = sel.xpath('/html/head/link[1]/@href')


            item = newsItem()

            try:
                date = sel.xpath('/html/body/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div[4]/div/div[1]/span[1]/text()')
                item['date'] = unicodedata.normalize('NFKD', date[0].extract()).encode('ascii', 'ignore')
            except:
                item['date'] = -1


            item['title'] = unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            item['link'] = unicodedata.normalize('NFKD', link[0].extract()).encode('ascii', 'ignore')
            item['author'] = unicodedata.normalize('NFKD', author[0].extract()).encode('ascii', 'ignore')
            item['publication'] = 'Aljazeera'
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
