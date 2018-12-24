# -*- coding: utf-8 -*-
import scrapy
from sinaDemo.items import SinademoItem
import os
import re
from copy import deepcopy

class SinaSpider(scrapy.Spider):

    name = 'sina'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):

        #获取到每一个大标题的data-sudaclick，用于区分大标题
        for each_topNames in response.xpath('//div[@class="clearfix"]/@data-sudaclick'):

            item = SinademoItem()
            topNames = "".join(each_topNames.extract())
            print(topNames)

            #进入到每一个大标题的小标题内
            for each_topName in response.xpath('//div[@data-sudaclick="'+ topNames + '"]'):

                top_titlename = each_topName.xpath('./h3/a/text()').extract()[0]
                top_titlelink = each_topName.xpath('./h3/a/@href').extract()[0]

                item['top_titlename'] = top_titlename
                item['top_titlelink'] = top_titlelink

                top_fileName  = './data/' + top_titlename

                if not (os.path.exists(top_fileName)):
                    os.makedirs(top_fileName)

                # print(top_titlename + top_titlelink)

                for each_secondname in each_topName.xpath('./ul/li/a'):

                    second_titlename = each_secondname.xpath('./text()').extract()[0]
                    second_titlelink = each_secondname.xpath('./@href').extract()[0]

                    item['second_titlename'] = second_titlename
                    item['second_titlelink'] = second_titlelink

                    top_secondName = top_fileName + '/' + second_titlename

                    if not (os.path.exists(top_secondName)):
                        os.mkdir(top_secondName)

                    # meta用于传输数据，这里将item传出去了
                    yield scrapy.Request(url=second_titlelink,meta={'meta_1':deepcopy(item)},callback = self.parse_artical)


    def parse_artical(self,response):
        item = response.meta['meta_1']

        for each in response.xpath('//a/@href'):
            mylink = "".join(each.extract())
            if mylink.endswith('.shtml'):
                if re.search('\d\d\d\d-\d\d-\d\d',mylink) != None:
                    yield scrapy.Request(url = mylink, meta = {"meta_2":deepcopy(item)},callback = self.parse_detail)


    def parse_detail(self,response):

        item = response.meta['meta_2']

        article_titlename = response.xpath('//h1[@class="main-title"]/text()').extract()[0]
        article_titlelink = response.url

        article_content = "".join(response.xpath('//div[@class="article"]/p/text()').extract())

        item['article_titlename'] = article_titlename
        item['article_titlelink'] = article_titlelink
        item['article_content'] = article_content.strip()

        yield item