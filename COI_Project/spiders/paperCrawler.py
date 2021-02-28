import codecs
import scrapy
import re
from COI_Project.items import CoiProjectItem
import ijson
import json
import os
import logging
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

    def __init__(self, json=None, itr_from=0 , offset=1, *args, **kwargs):
        super(PapercrawlerSpider, self).__init__(*args, **kwargs)
        if json == None:
            print("No Json file specified")
        self.counter = 0
        self.json = json
        self.search_keyword = ''
        self.itr_from = int(itr_from)
        self.offset = int(offset)
        logger = self.logger_config(log_path='log.txt', logging_name='paperCrawler')
        logger.info("Start from paper no.{} to paper no.{}(not include) with offset={}".format(self.itr_from,self.itr_from+self.offset,self.offset))

    def start_requests(self):
        try:
            with open(self.json, 'r', encoding='UTF-8') as f:
                citations = ijson.items(f, 'item')
                for i in range(self.itr_from):
                    next(citations)
                cnt = self.itr_from;
                for paper in citations:
                    # print(str(cnt)+": ", end='')
                    cnt = cnt + 1
                    if cnt > self.itr_from+self.offset:
                        return
                    names = []
                    # if paper['authors']:
                    #     for person in paper['authors']:
                    #         names.append(person['name'])
                    if paper['title']:
                        self.search_keyword = paper['title']
                        for name in names:
                            self.search_keyword = self.search_keyword+', '+name
                        # print(self.search_keyword)
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
        self.counter = self.counter + 1
        # print(response.request.headers)
        # print(response.request.meta)
        URLs = response.css('a::attr(href)').extract()
        # contents = response.css('a::text').extract()
        # idx = -1
        for url in URLs:
            # idx = idx + 1
            match = re.search('http.*pdf',url)
            if match:
                abstract0 = ''.join(response.css('div[data-rp="0"] .gs_rs::text').extract())
                abstract1 = ''
                try:
                    abstract1 = ''.join(response.css('div[data-rp="0"] .gs_rs b::text').extract())
                except:
                    pass
                abstract = abstract0 + abstract1
                curPaper['abstract'] = abstract
                try:
                    return scrapy.Request(url=match.group(0), callback=lambda response, curPaper=curPaper: self.parse_paper(response,curPaper))
                except Exception as e:
                    print('\rException happens in {}'.format(url)+str(e))
                    continue
        root = './json'
        path = root + '/wait4FurtherCrawler.json'
        try:
            if not os.path.exists(root):
                os.mkdir(root)
            if not os.path.exists(path):
                with open(path,'w', encoding='UTF-8') as f:
                    json.dump(curPaper, f,cls=DecimalEncoder)
                    f.close()
            else:
                with open(path,'a', encoding='UTF-8') as f:
                    f.write(',\n')
                    json.dump(curPaper, f, cls=DecimalEncoder)
                    f.close()
        except Exception as e:
            print('Exception in file I/O: {}'.format(str(e)))


    def parse_paper(self,response, curPaper):
        if response.status != 200:
            if curPaper['abstract']:
                curPaper.pop('abstract')
            root = './json'
            path = root + '/wait4FurtherCrawler.json'
            try:
                if not os.path.exists(root):
                    os.mkdir(root)
                if not os.path.exists(path):
                    with open(path, 'w', encoding='UTF-8') as f:
                        json.dump(curPaper, f,cls=DecimalEncoder)
                        f.close()
                else:
                    with open(path, 'a', encoding='UTF-8') as f:
                        f.write(',\n')
                        json.dump(curPaper, f, cls=DecimalEncoder)
                        f.close()
            except:
                print('Exception in file I/O')
            return
        # request_url = response.request.url
        item = CoiProjectItem()
        item['counter'] = str(self.counter)
        item['fileName'] = str(curPaper['id'])
        item['content'] = response.body
        item['authors'] = curPaper['authors']
        item['title'] = curPaper['title']
        item['abstract'] = curPaper['abstract']
        yield item

    def logger_config(self, log_path, logging_name):
        '''
        config log
        :param log_path: output log path
        :param logging_name: record name，optional
        :return:
        '''

        logger = logging.getLogger(logging_name)
        logger.setLevel(level=logging.DEBUG)

        handler = logging.FileHandler(log_path, encoding='UTF-8')
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)

        logger.addHandler(handler)
        logger.addHandler(console)
        return logger

    def unmangle_utf8(self, match):
        escaped = match.group(0)  # '\\u00e2\\u0082\\u00ac'
        hexstr = escaped.replace(r'\u00', '')  # 'e282ac'
        buffer = codecs.decode(hexstr, "hex")  # b'\xe2\x82\xac'

        try:
            return buffer.decode('utf8')  # '€'
        except UnicodeDecodeError:
            print("Could not decode buffer: %s" % buffer)
