from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from crawlers.items import newsItem
import unicodedata

class NationalReview(CrawlSpider):
    name = "nationalReview"
    allowed_domains = ["nationalreview.com"]
    start_urls = ["http://www.nationalreview.com", "http://www.nationalreview.com/corner"]

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=['//*[@id="scroll600_otd_show_hide"]/a']),callback='parse_item', follow=True),
        )

    def parse_item(self, response):
        try:
            sel = Selector(response)
            #print response
            title = sel.xpath('//*[@id="font-size26"]/text()')
            #print '           '
            #print unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            #print '           '
            author = sel.xpath('//*[@id="author-wrapper"]/div/a/span/text()')
            #content = sel.xpath('//*[@id="story"]/p[1]/text()') #List
            # //*[@id="article_text"]/div/div/div/div/p[1]/span[1]/text()
            # sel.xpath('//*[@id="article_text"]/div/div/div/div/p/text()')
            content = sel.xpath('//*[@id="article_text"]/div/div/div/div/p/text()')
            link = sel.xpath('/html/head/link[2]/@href')


            item = newsItem()

            try:
                date = sel.xpath('//*[@id="node-375166"]/div[1]/span/text()')
                item['date'] = unicodedata.normalize('NFKD', date[0].extract()).encode('ascii', 'ignore')
            except:
                item['date'] = -1

            item['title'] = unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            item['link'] = unicodedata.normalize('NFKD', link[0].extract()).encode('ascii', 'ignore')
            item['author'] = unicodedata.normalize('NFKD', author[0].extract()).encode('ascii', 'ignore')
            item['publication'] = 'National Review'
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
