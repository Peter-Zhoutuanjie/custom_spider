# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CustomItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class TradeGoodsItem(scrapy.Item):
    month = scrapy.Field()
    goods_code = scrapy.Field()
    goods = scrapy.Field()
    partner_code = scrapy.Field()
    partner_name = scrapy.Field()
    port_code = scrapy.Field()
    port_name = scrapy.Field()
    first_num = scrapy.Field()
    first_unit = scrapy.Field()
    second_num = scrapy.Field()
    second_unit = scrapy.Field()
    price = scrapy.Field()
    ie_type = scrapy.Field()


class TradeGoodsPortItem(scrapy.Item):
    month = scrapy.Field()
    goods_code = scrapy.Field()
    goods = scrapy.Field()
    port_code = scrapy.Field()
    port_name = scrapy.Field()
    first_num = scrapy.Field()
    first_unit = scrapy.Field()
    second_num = scrapy.Field()
    second_unit = scrapy.Field()
    price = scrapy.Field()
    ie_type = scrapy.Field()


class TradeGoodsPartnerItem(scrapy.Item):
    month = scrapy.Field()
    goods_code = scrapy.Field()
    goods = scrapy.Field()
    partner_code = scrapy.Field()
    partner_name = scrapy.Field()
    port_code = scrapy.Field()
    port_name = scrapy.Field()
    first_num = scrapy.Field()
    first_unit = scrapy.Field()
    second_num = scrapy.Field()
    second_unit = scrapy.Field()
    price = scrapy.Field()
    ie_type = scrapy.Field()


class GoodsCodeItem(scrapy.Item):
    code_length = scrapy.Field()
    code = scrapy.Field()
    name = scrapy.Field()
    year_id = scrapy.Field()
    first_unit_code = scrapy.Field()
    first_unit_name = scrapy.Field()
    second_unit_code = scrapy.Field()
    second_unit_name = scrapy.Field()
