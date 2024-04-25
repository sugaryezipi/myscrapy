# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RenewScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
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


class ShangPinItem(Item):
    detail_name = Field()
    produced_at = Field()
    description = Field()
    price = Field()
    page = Field()
    name = Field()
    created_at = Field()
    cur_page = Field()
