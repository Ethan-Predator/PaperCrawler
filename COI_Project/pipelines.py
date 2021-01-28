# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class CoiProjectPipeline:
    def process_item(self, item, spider):
        if item['fileName']:
            try:
                with open(item['fileName']+'.pdf','wb') as f:
                    f.write(item['content'])
                    f.close()
                    print("download successfully")
                    return item
            except:
                print('fail to download')
                return item

        else:
            return DropItem("Missing Text")
