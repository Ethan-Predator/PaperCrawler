import scrapy
import re
from COI_Project.items import CoiProjectItem
import ijson

class PapercrawlerSpider(scrapy.Spider):
    name = 'paperCrawler'
    # allowed_domains = ['google.com']
    # search_keyword = 'Bitcoin: A Peer-to-Peer Electronic Cash System'
    # start_urls = ['https://www.bing.com/search?q='+search_keyword]

    def __init__(self, json=None, *args, **kwargs):
        super(PapercrawlerSpider, self).__init__(*args, **kwargs)
        self.json = json
        self.search_keyword = ''

    def start_requests(self):
        try:
            with open(self.json, 'r', encoding='utf-8') as f:
                citations = ijson.items(f, 'item')
                # papers = (paper for paper in citations if citations['title'])
                # cnt = 0;
                for paper in citations:
                    # cnt = cnt + 1
                    # if cnt > 10:
                    #     return
                    if paper['title']:
                        self.search_keyword = paper['title']
                        urls = [
                                'https://www.bing.com/search?q={}'.format(self.search_keyword)
                        ]
                        for url in urls:
                            yield scrapy.Request(url = url, callback=self.parse)
        except Exception as e:
            print(str(e))
            # print("cannot open the file {}".format(self.json))
            return


    def parse(self, response):
        URLs = response.css('a::attr(href)').extract()
        # pattern = re.compile('^http.*pdf')
        for url in URLs:
            match = re.search('http.*pdf',url)
            if match:
                # print(match.group(0))
                try:
                    yield scrapy.Request(url=url, callback=self.parse_paper)
                except Exception as e:
                    print('\rException happens in {}'.format(url)+str(e))
                    continue

    def parse_paper(self,response):
        if response.status != 200:
            return
        request_url = response.request.url
        item = CoiProjectItem()
        item['fileName'] = request_url.split('/')[-1][:-4]
        item['content'] = response.body
        yield item
