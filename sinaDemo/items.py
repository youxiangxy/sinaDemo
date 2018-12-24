# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinademoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    #大分类标题名和链接
    top_titlename = scrapy.Field()
    top_titlelink = scrapy.Field()

    #小分类标题名和链接
    second_titlename = scrapy.Field()
    second_titlelink = scrapy.Field()

    #文章标题、链接和内容
    article_titlename = scrapy.Field()
    article_titlelink = scrapy.Field()
    article_content = scrapy.Field()