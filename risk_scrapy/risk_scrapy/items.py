# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy import Field, Item

class NewsItem(Item):
    title = Field()
    text = Field()
    datetime = Field()
    source = Field()
    url = Field()
    website = Field()
    page = Field()
    name = Field()
    date = Field()