import scrapy
import os
from ecom_price_crawler.items import ProductItem, AttributeItem
from urllib.parse import urlencode, urljoin
from datetime import datetime
from scrapy.loader import ItemLoader

class EbaySpider(scrapy.Spider):
    name = 'ebay'
    allowed_domains = ['www.ebay.com']
    os.environ["http_proxy"] = "http://185.199.231.45:8382"
    
    def start_requests(self):
        queries = ['pillow']
        for query in queries:
            url = 'https://www.ebay.com/sch/i.html?' + urlencode({'_nkw': query})
            yield scrapy.Request(url=url, callback=self.parse, meta={'query': query})

    def parse(self, response):
        query = response.meta['query']
        products = response.xpath('//li[contains(@class, "s-item ")]')
        for product in products:
            product_loader = ItemLoader(item=ProductItem(), selector=product, response=response)
            product_loader.add_value('site_name', self.allowed_domains[0])
            # product_loader.add_xpath('product_identification_number', './/@data-item-id')
            product_loader.add_xpath('title', './/h3[@class="s-item__title"]/text()')
            product_loader.add_xpath('image_src', './/img[contains(@class, "s-item__image-img")]/@src')
            product_loader.add_xpath('rating', './/div[contains(@class, "b-starrating")]/span[1]/text()')
            product_loader.add_xpath('price', './/span[contains(@class, "s-item__price")]/text()')
            product_loader.add_xpath('product_url', './/a[contains(@class, "s-item__link")]/@href')
            product_loader.add_xpath('description', './/div[@class="s-item__subtitle"]/text()')
            reviews_url = product_loader.get_xpath('.//a[contains(@class, "s-item__reviews")]//@href')
            if reviews_url:
                product_loader.add_value('reviews', urljoin(response.url, reviews_url[0]))
            attributes = product.xpath('.//div[@class="s-item__detail s-item__detail--primary"]//li')
            attribute_items = []
            for attribute in attributes:
                attribute_loader = ItemLoader(item=AttributeItem(), selector=attribute, response=response)
                attribute_loader.add_xpath('title', './/span[@class="s-label-popover"]/text()')
                attribute_loader.add_xpath('value', './/span[@class="s-item__dynamic s-item__dynamicAttributes1"]/text()')
                attribute_items.append(attribute_loader.load_item())
            product_loader.add_value('attributes', attribute_items)
            yield product_loader.load_item()

        next_page_url = response.xpath('//a[@class="pagination__next"]/@href')
        if next_page_url:
            yield scrapy.Request(url=urljoin(response.url, next_page_url[0].extract()), callback=self.parse, meta={'query': query})
