# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class TechcrawlItem(Item):
    title = Field()
    url = Field()
    headers = Field()
    domain = Field()
    pagerank = Field()
    score_added = Field()
    have_added = Field()
    body = Field()
