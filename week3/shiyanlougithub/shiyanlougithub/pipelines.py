# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime
from sqlalchemy.orm import sessionmaker
from shiyanlougithub.models import Repository, engine

class ShiyanlouPipeline(object):
    def process_item(self, item, spider):
        item['update_time'] = datetime.strptime(
                item['update_time'], '%Y-%m-%dT%H:%M:%SZ')
        if item['commits'] is not None:
            if ',' in item['commits']:
                num_list=item['commits'].split(',')
                item['commits']=int(num_list[0]+num_list[1])
            else:
                item['commits']=int(item['commits'])
        if item['branches'] is not None:
            if ',' in item['branches']:
                num_list=item['branches'].split(',')
                item['branches']=int(num_list[0]+num_list[1])
            else:
                item['branches']=int(item['branches'])
        if item['releases'] is not None:
            if ',' in item['releases']:
                num_list=item['releases'].split(',')
                item['releases']=int(num_list[0]+num_list[1])
            else:
                item['releases']=int(item['releases'])
        self.session.add(Repository(**item))
        return item

    def open_spider(self, spider):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

