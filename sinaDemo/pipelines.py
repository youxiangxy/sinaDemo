# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import os

class SinademoPipeline(object):

    def process_item(self, item, spider):
        date = re.search('\d\d\d\d-\d\d-\d\d',item['article_titlelink']).group()

        path = './data/' + item['top_titlename'] +'/' + item['second_titlename'] + "/" + date

        if not (os.path.exists(path)):
            os.makedirs(path)

        f = open(path + "/" + item['article_titlename'] + '.txt','w',encoding="utf-8")

        f.write(item['article_content'])
        f.close()

        return item
