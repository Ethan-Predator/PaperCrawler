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
sys.path.append("./COI_Project/lib")
from DecimalEncoder import DecimalEncoder

class CoiProjectPipeline:
    def process_item(self, item, spider):
        if item['fileName']:
            root = './papers&metadata'
            try:
                if not os.path.exists(root):
                    os.mkdir(root)
            except Exception as e:
                print('Exception: file I/O in pipelines.py: {}'.format(str(e)))
            try:
                with open('./papers&metadata/'+item['fileName'] + '.meta', 'w', encoding='UTF-8') as f:
                    paper_dic = {'title':item['title'], 'authors':item['authors'], 'abstract':item['abstract']}
                    json.dump(paper_dic, f, cls=DecimalEncoder)
                    f.close()
                    print("\r{}.meta >> download successfully --- cnt:{}".format(item['fileName'], item['counter']))
            except Exception as e:
                print("\r{}.meta >> download UNsuccessfully --- {}".format(item['fileName'], str(e)))
            try:
                with open('./papers&metadata/'+item['fileName']+'.pdf','wb') as f:
                    f.write(item['content'])
                    f.close()
                    print("\r{}.pdf >> download successfully".format(item['fileName']))
                    return item
            except Exception as e:
                print("\r{}.pdf >> download UNsuccessfully --- {}".format(item['fileName'],str(e)))
                return item

        else:
            return DropItem("Missing Text")
