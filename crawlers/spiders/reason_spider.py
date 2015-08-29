from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor


from crawlers.items import newsItem
import unicodedata
import datetime

class nyt(CrawlSpider):
    now = datetime.datetime.now() + datetime.timedelta(days=1)
    name = "reason"
    allowed_domains = ["reason.com"]
    start_urls = [
    "http://reason.com/search?_[pubdate_to]=" + now.strftime("%Y-%m-%d") + "%2012:10:00&f[pubdate]=c&q=+&s=-pubdate",
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths=['//*[@id="content-col"]/section[2]/article/header/h2/a']),callback='parse_item', follow=True),
        )

    def parse_item(self, response):
        now = datetime.datetime.now() + datetime.timedelta(days=1)
        print "http://reason.com/search?_[pubdate_to]=" + now.strftime("%Y-%m-%d") + "%2012:10:00&f[pubdate]=c&q=+&s=-pubdate\n\n\n" 
        try:
            sel = Selector(response)
            #print response
            title = sel.xpath('//*[@id="content-col"]/article/header/h2[1]/a/text()')
            #print '           '
            #print unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            #print '           '
            author = sel.xpath('//*[@id="content-col"]/article/header/p/a/text()')
            #content = sel.xpath('//*[@id="story"]/p[1]/text()') #List
            content = sel.xpath('//*[@id="content-col"]/article/div[1]/div/p/text()')
            link = sel.xpath('//*[@id="content-col"]/article/header/h2[1]/a/@href')

            item = newsItem()

            try:
                date = sel.xpath('//*[@id="content-col"]/article/header/p/time/text()').split("by")[0]
                item['date'] = unicodedata.normalize('NFKD', date[0].extract()).encode('ascii', 'ignore')
            except:
                item['date'] = -1

            item['title'] = unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            item['link'] = unicodedata.normalize('NFKD', link[0].extract()).encode('ascii', 'ignore')
            item['author'] = unicodedata.normalize('NFKD', author[0].extract()).encode('ascii', 'ignore')
            item['publication'] = 'Reason'
            item['politicalScore'] = 100
            item['posNegScore'] = 0
            wholeBody = ''
            for part in content:
                wholeBody += unicodedata.normalize('NFKD', part.extract()).encode('ascii', 'ignore')
            item['body'] = unicodedata.normalize('NFKD', content[0].extract()).encode('ascii', 'ignore')
            item['body'] = wholeBody
            #print(link)

            return [item]
        except:
            print("res" + str(response))
            return []
