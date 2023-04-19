# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class ProductItem(Item):
    site_name = scrapy.Field()
    product_identification_number = scrapy.Field()
    title = scrapy.Field()
    image_src = scrapy.Field()
    rating = scrapy.Field()
    price = scrapy.Field()
    product_url = scrapy.Field()
    description = scrapy.Field()
    reviews = scrapy.Field()
    attributes = scrapy.Field()
    
class AttributeItem(Item):
    title = scrapy.Field()
    value = scrapy.Field()