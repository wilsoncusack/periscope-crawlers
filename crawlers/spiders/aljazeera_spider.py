from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from crawlers.items import newsItem
import unicodedata

class Aljazeera(CrawlSpider):
    name = "Aljazeera"
    allowed_domains = ["america.aljazeera.com/", "aljazeera.com"]
    start_urls = ["http://america.aljazeera.com/opinions.html", "http://america.aljazeera.com/", "http://america.aljazeera.com/topics/topic/categories/us.html", "http://america.aljazeera.com/topics/topic/categories/international.html", "http://america.aljazeera.com/topics/topic/categories/economy.html", "http://america.aljazeera.com/topics/topic/categories/technology.html", "http://america.aljazeera.com/topics/topic/categories/science.html", "http://america.aljazeera.com/topics/topic/categories/environment.html", "http://america.aljazeera.com/topics/topic/categories/sports.html", "http://america.aljazeera.com/topics/topic/categories/culture.html", "http://america.aljazeera.com/topics/topic/issue/human-rights.html"]

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=['/html/body/div[2]/div[3]/div/div[1]/div[1]/div[1]/section/div/div/article/h1/a', '/html/body/div[2]/div[3]/div/div[1]/div[1]/div[1]/section/div/div/div/article/div/h2/a', '//*[@id="articleHighlightList-0"]/div/div/div/article/div[2]/h3/a', '/html/body/div[2]/div[3]/div/div[2]/div[1]/div[1]/div[3]/div/div[2]/div/a', '/html/body/div[2]/div[3]/div/div[2]/div[1]/div[2]/div/div[2]/div/div/a', '/html/body/div[2]/div[1]/div/div[1]/div/div/div/div[2]/section/div[1]/div/div/article/div[2]/h3/a', '/html/body/div[2]/div[1]/div/div[1]/div/div/div/div[1]/div/div/div[2]/section/div/div[2]/article/h1/a', '/html/body/div[2]/div[1]/div/div[1]/div/div/div/div[1]/div/div/div[2]/section/div/div[2]/div/article/div/h2/a', '//*[@id="articleHighlightList-0"]/div/div/div[2]/article/div[2]/h3/a']),callback='parse_item', follow=True),
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
