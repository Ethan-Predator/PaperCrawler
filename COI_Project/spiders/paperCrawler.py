import scrapy
import re
from COI_Project.items import CoiProjectItem

class PapercrawlerSpider(scrapy.Spider):
    name = 'paperCrawler'
    # allowed_domains = ['google.com']
    search_keyword = 'Bitcoin: A Peer-to-Peer Electronic Cash System'
    start_urls = ['https://www.bing.com/search?q='+search_keyword]

    def parse(self, response):
        URLs = response.css('a::attr(href)').extract()
        # pattern = re.compile('^http.*pdf')
        for url in URLs:
            match = re.search('http.*pdf',url)
            if match:
                print(match.group(0))
                try:
                    yield scrapy.Request(url=url, callback=self.parse_paper)
                except:
                    continue

    def parse_paper(self,response):
        if response.status != 200:
            return
        item = CoiProjectItem()
        item['fileName'] = '1'
        item['content'] = response.body
        yield item
        # try:
        #     with open('abc.pdf','wb') as f:
        #         f.write(response.body)
        #         f.close()
        #         print("download successfully")
        # except:
        #     print('fail to download')
