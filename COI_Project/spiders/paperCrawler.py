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
                cnt = 0;
                for paper in citations:
                    cnt = cnt + 1
                    if cnt > 5:
                        return
                    names = []
                    # if paper['authors']:
                    #     for person in paper['authors']:
                    #         names.append(person['name'])
                    if paper['title']:
                        self.search_keyword = paper['title']
                        for name in names:
                            self.search_keyword = self.search_keyword+', '+name
                        print(self.search_keyword)
                        urls = [
                                'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q='+self.search_keyword+'&btnG='
                        ]
                        for url in urls:
                            yield scrapy.Request(url = url, callback=lambda response: self.parse(response))
        except TypeError:
            pass
        except Exception as e:
            print(str(e))
            # print("cannot open the file {}".format(self.json))
            return


    def parse(self, response):
        URLs = response.css('a::attr(href)').extract()
        contents = response.css('a::text').extract()
        idx = -1
        for url in URLs:
            idx = idx + 1
            match = re.search('http.*pdf',url)
            if match:
                # print(match.group(0))
                try:
                    yield scrapy.Request(url=url, callback=self.parse_paper)
                except Exception as e:
                    print('\rException happens in {}'.format(url)+str(e))
                    continue
            # else:
            #     print(contents[idx])


    def parse_paper(self,response):
        if response.status != 200:
            return
        request_url = response.request.url
        item = CoiProjectItem()
        item['fileName'] = request_url.split('/')[-1][:-4]
        item['content'] = response.body
        yield item
