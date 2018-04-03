# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class DzdpItem(scrapy.Item):
    shop_id = scrapy.Field()
    shop_name = scrapy.Field()
    shop_img_address = scrapy.Field()
    shop_poi = scrapy.Field()
    shop_stars = scrapy.Field()
    shop_sorce = scrapy.Field()
    shop_address = scrapy.Field()
    shop_phone = scrapy.Field()
    shop_phone1 = scrapy.Field()
    shop_charge = scrapy.Field()
    mean_price = scrapy.Field()
    shop_time = scrapy.Field()
    shop_service = scrapy.Field()
    shop_info = scrapy.Field()
    channel_type = scrapy.Field()
    create_time = scrapy.Field()
    pay_play = scrapy.Field()
    shop_park = scrapy.Field()
    comment = scrapy.Field()
    shop_type = scrapy.Field()

class ContentItem(scrapy.Item):
    shop_id = scrapy.Field()
    user_name = scrapy.Field()
    content_stars = scrapy.Field()
    content_sorce = scrapy.Field()
    user_content = scrapy.Field()
    channel_type = scrapy.Field()

