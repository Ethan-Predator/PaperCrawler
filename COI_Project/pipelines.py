# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import json
import sys
import os
import logging
sys.path.append("./COI_Project/lib")
from DecimalEncoder import DecimalEncoder

class CoiProjectPipeline:
    def __init__(self):
        self.logger = self.logger_config(log_path='paper_log.txt', logging_name='paperPipelines')

    def process_item(self, item, spider):
        if item['fileName']:
            root = './papers&metadata'
            try:
                if not os.path.exists(root):
                    os.mkdir(root)
            except Exception as e:
                self.logger.info('Exception: file I/O in pipelines.py: {}'.format(str(e)))
            try:
                with open('./papers&metadata/'+item['fileName'] + '.meta', 'w', encoding='UTF-8') as f:
                    paper_dic = {'title':item['title'], 'authors':item['authors'], 'abstract':item['abstract']}
                    json.dump(paper_dic, f, cls=DecimalEncoder)
                    f.close()
                    self.logger.info("{}.meta >> download successfully --- cnt:{}".format(item['fileName'], item['counter']))
            except Exception as e:
                self.logger.info("{}.meta >> download UNsuccessfully --- {}".format(item['fileName'], str(e)))
            try:
                with open('./papers&metadata/'+item['fileName']+'.pdf','wb') as f:
                    f.write(item['content'])
                    f.close()
                    self.logger.info("{}.pdf >> download successfully".format(item['fileName']))
                    return item
            except Exception as e:
                self.logger.info("{}.pdf >> download UNsuccessfully --- {}".format(item['fileName'],str(e)))
                return item

        else:
            return DropItem("Missing Text")

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
