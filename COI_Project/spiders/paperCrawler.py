import scrapy
import re
from COI_Project.items import CoiProjectItem
import ijson
import json
import os
# import decimal
import sys
sys.path.append("./COI_Project/lib")
from DecimalEncoder import DecimalEncoder
# class DecimalEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, decimal.Decimal):
#             return str(o)
#         return super(DecimalEncoder, self).default(o)

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
            with open(self.json, 'r', encoding='ISO-8859-1') as f:
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
                            yield scrapy.Request(url = url, callback=lambda response, curPaper=paper: self.parse(response,curPaper))
        except TypeError:
            pass
        except Exception as e:
            print(str(e))
            # print("cannot open the file {}".format(self.json))
            return


    def parse(self, response, curPaper):
        URLs = response.css('a::attr(href)').extract()
        # contents = response.css('a::text').extract()
        # idx = -1
        for url in URLs:
            # idx = idx + 1
            match = re.search('http.*pdf',url)
            if match:
                # print(match.group(0))
                try:
                    print("before return:"+url)
                    return scrapy.Request(url=url, callback=lambda response, curPaper=curPaper: self.parse_paper(response,curPaper))
                except Exception as e:
                    print('\rException happens in {}'.format(url)+str(e))
                    continue
        root = './json'
        path = root + '/wait4FurtherCrawler.json'
        try:
            if not os.path.exists(root):
                os.mkdir(root)
            if not os.path.exists(path):
                with open(path,'w', encoding='ISO-8859-1') as f:
                    json.dump(curPaper, f,cls=DecimalEncoder)
                    f.close()
            else:
                with open(path,'a', encoding='ISO-8859-1') as f:
                    f.write(',\n')
                    json.dump(curPaper, f,cls=DecimalEncoder)
                    f.close()
        except Exception as e:
            print('Exception in file I/O: {}'.format(str(e)))


    def parse_paper(self,response, curPaper):
        print('before check')
        if response.status != 200:
            root = './json'
            path = root + '/wait4FurtherCrawler.json'
            try:
                if not os.path.exists(root):
                    os.mkdir(root)
                if not os.path.exists(path):
                    with open(path, 'w', encoding='ISO-8859-1') as f:
                        json.dump(curPaper, f,cls=DecimalEncoder)
                        f.close()
                else:
                    with open(path, 'a', encoding='ISO-8859-1') as f:
                        f.write(',\n')
                        json.dump(curPaper, f,cls=DecimalEncoder)
                        f.close()
            except:
                print('Exception in file I/O')
            return
        print('after check')
        request_url = response.request.url
        item = CoiProjectItem()
        item['fileName'] = request_url.split('/')[-1][:-4]
        item['content'] = response.body
        yield item
