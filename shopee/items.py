# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# shopee网站爬虫
class ParentItem(scrapy.Item):
    # define the fields for your item here like:
    catid = scrapy.Field()
    display_name = scrapy.Field()
    second_url = scrapy.Field()
    child_cat_list = scrapy.Field()
    second_cage_catid = scrapy.Field()
    second_cage_display_name = scrapy.Field()


class ChildItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    category= scrapy.Field()
    title = scrapy.Field()
    image = scrapy.Field()
    price = scrapy.Field()
    Num_sell = scrapy.Field()
    id=scrapy.Field()
    like_count=scrapy.Field()
    tablename=scrapy.Field()
    # 类别
