# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VerifybuildlistItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    branchx = scrapy.Field()
    branch_project_l = scrapy.Field()

