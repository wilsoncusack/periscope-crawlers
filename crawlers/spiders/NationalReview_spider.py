from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor

from crawlers.items import newsItem
import unicodedata

class NationalReview(CrawlSpider):
    name = "nationalReview"
    allowed_domains = ["nationalreview.com"]
    start_urls = ["http://www.nationalreview.com", "http://www.nationalreview.com/corner"]

    rules = (
        Rule(LinkExtractor(restrict_xpaths=['/html/body/div[4]/div[1]/div[1]/div/div/div/header/h1/a','/html/body/div[3]/div/div[1]/div/div/div/ul/li[1]/div/div[1]/div[2]/div[2]/div/div/a','/html/body/div[3]/div/div[1]/div/div/div/ul/li[1]/div/div[1]/div[2]/div[1]/div/div/a', '/html/body/div[3]/div/div[1]/div/div/div/ul/li[1]/div/div[1]/div/div/div/a']),callback='parse_item', follow=True),
        )
    # /html/body/div[3]/div/div[1]/div/div/div/ul/li[1]/div/div[1]/div[2]/div[1]/div[1]/div/a
    # /html/body/div[3]/div/div[1]/div/div/div/ul/li[1]/div/div[1]/div[2]/div[1]/div[2]/div/a
    # /html/body/div[3]/div/div[1]/div/div/div/ul/li[1]/div/div[1]/div[3]/div[4]/div/a
    # /html/body/div[3]/div/div[1]/div/div/div/ul/li[1]/div/div[1]/div[4]/div[1]/div/a


    def parse_item(self, response):
        try:
            sel = Selector(response)
            #print response
            try:
                title = sel.xpath('/html/body/div[5]/div[1]/div[1]/div/div[1]/div/header/h1/a/text()')
            except:
                # for the corner, not working
                title = sel.xpath('/html/body/div[4]/div[1]/div[1]/div/div[2]/div/header/h1/a/text()')
            
            #print '           '
            #print unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            #print '           '
            author = sel.xpath('/html/body/div[5]/div[1]/div[1]/div/div[1]/div/div[4]/div[1]/div/div[2]/span/a/text()')
            #content = sel.xpath('//*[@id="story"]/p[1]/text()') #List
            # //*[@id="article_text"]/div/div/div/div/p[1]/span[1]/text()
            # sel.xpath('//*[@id="article_text"]/div/div/div/div/p/text()')
            content = sel.xpath('/html/body/div[5]/div[1]/div[1]/div/div[1]/div/div[4]/div[1]/div/p/text()')
            link = sel.xpath('/html/body/div[5]/div[1]/div[1]/div/div[1]/div/header/h1/a/@href')


            item = newsItem()

            try:
                date = sel.xpath('/html/body/div[5]/div[1]/div[1]/div/div[1]/div/div[4]/div[1]/div/div[2]/time/text()')
                item['date'] = unicodedata.normalize('NFKD', date[0].extract()).encode('ascii', 'ignore')
            except:
                item['date'] = -1

            item['title'] = unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            item['link'] = unicodedata.normalize('NFKD', link[0].extract()).encode('ascii', 'ignore')
            item['author'] = unicodedata.normalize('NFKD', author[0].extract()).encode('ascii', 'ignore')
            item['publication'] = 'National Review'
            item['politicalScore'] = 150
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
