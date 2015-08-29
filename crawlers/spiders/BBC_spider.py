from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor

from crawlers.items import newsItem
import unicodedata

class bbc(CrawlSpider):
    name = "bbc"
    allowed_domains = ["bbc.co.uk","bbc.com"]
    start_urls = ["https://www.bbc.co.uk/", "https://www.bbc.com/news/", "https://www.bbc.com/news/world/us_and_canada/", "https://www.bbc.com/news/world/latin_america/", "https://www.bbc.com/news/uk/", "https://www.bbc.com/news/world/africa/", "https://www.bbc.com/news/world/asia/", "https://www.bbc.com/news/world/europe/", "https://www.bbc.com/news/world/middle_east/", "https://www.bbc.com/news/business/", "https://www.bbc.com/news/health/", "https://www.bbc.com/news/science_and_environment/", "https://www.bbc.com/news/technology/", "https://www.bbc.com/news/entertainment_and_arts/"]

    rules = (
        Rule(LinkExtractor(restrict_xpaths=['//*[@id="news_hero"]/div/a','//*[@id="news_hero_mini"]/div/a', '//*[@id="news_moreTopStories"]/ul/li/a', '//*[@id="promo2_carousel_items"]/dl/dt/a', '//*[@id="business_hero_mini"]/div/a', '//*[@id="business_moreTopStories"]/ul/li/a', '//*[@id="sport_hero_mini"]/div/a', '//*[@id="sport_moreTopStories"]/ul/li/a', '//*[@id="more_entertainment_hero"]/div/a', '//*[@id="more_health_hero"]/div/a', '//*[@id="more_technology_hero"]/div/a', '//*[@id="more_science_hero"]/div/a', '//*[@id="capital_hero"]/div/a', '//*[@id="capital_list"]/ul/li/a', '//*[@id="autos_hero"]/div/a', '//*[@id="autos_list"]/ul/li/a', '//*[@id="culture_hero"]/div/a', '//*[@id="future_hero"]/div/a', '//*[@id="future_list"]/ul/li/a', '//*[@id="travel_hero"]/div/a', '//*[@id="travel_list"]/ul/li/a', '//*[@id="top-story"]/h2/a', '//*[@id="second-story"]/div/h2/a', '//*[@id="third-story"]/div/h2/a','//*[@id="other-top-stories"]/ul/li/h3/a']),callback='parse_item', follow=True),
        )

    def parse_item(self, response):
        try:
            sel = Selector(response)
            #print response
            title = sel.xpath('//*[@id="main-content"]/div[2]/div[1]/h1/text()')
            #print '           '
            #print unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            #print '           '
            #try:
            #    author = sel.xpath('//*[@id="story-header"]/div/div/p/span/a/span/text()')
            #    item['author'] = unicodedata.normalize('NFKD', author[0].extract()).encode('ascii', 'ignore')
            #except:
            #    item['author'] = ''
                
            #content = sel.xpath('//*[@id="story"]/p[1]/text()') #List
            content = sel.xpath('//*[@id="main-content"]/div/div/p/text()')
            link = sel.xpath('/html/head/link[1]/@href')


            item = newsItem()

            try:
                date = sel.xpath('//*[@id="main-content"]/div[2]/div[1]/span[1]/span[1]/text()')
                item['date'] = unicodedata.normalize('NFKD', date[0].extract()).encode('ascii', 'ignore')
            except:
                item['date'] = -1


            item['title'] = unicodedata.normalize('NFKD', title[0].extract()).encode('ascii', 'ignore')
            item['link'] = unicodedata.normalize('NFKD', link[0].extract()).encode('ascii', 'ignore')
            item['author'] = '' #unicodedata.normalize('NFKD', author[0].extract()).encode('ascii', 'ignore')
            item['publication'] = 'BBC'
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
