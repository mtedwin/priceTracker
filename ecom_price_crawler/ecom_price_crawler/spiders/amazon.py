import os
import re
import json
from urllib.parse import urlencode, urljoin
import scrapy
from datetime import datetime
from ecom_price_crawler.items import ProductItem, AttributeItem

# Pass in more keywords here if necessary
queries = ['pillow']

class AmazonSpider(scrapy.Spider):
    name="amazon"
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/']
    os.environ["http_proxy"] = "http://185.199.231.45:8382"

    def url_header(self):
           headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    def start_requests(self):
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        for query in queries:
            url = 'https://www.amazon.com/s?' + urlencode({'k': query})
            yield scrapy.Request(url=url, callback=self.parse_keyword_response , headers=headers)
            
    def parse_keyword_response(self, response):
        products = response.xpath('//*[@data-asin]')

        for product in products:
            asin = product.xpath('@data-asin').extract_first()
            if not asin:
                continue
            product_url = f"https://www.amazon.com/dp/{asin}"
            yield scrapy.Request(url=product_url, callback=self.parse_product_page, meta={'asin': asin })

        next_page = response.xpath('//li[@class="a-last"]/a/@href').extract_first()
        if next_page:
            url = urljoin("https://www.amazon.com",next_page)
            yield scrapy.Request(url=product_url, callback=self.parse_keyword_response)
            
                
    def parse_review_page(self, response):
        # retrieve item generated in previous request
        item = response.meta['item']
        
        reference_id = response.xpath('//div[@data-hook="review"]/@id').extract()
        titles = response.xpath('//a[@data-hook="review-title"]/span/text()').extract()
        ratings = response.xpath('//span[@class="a-icon-alt"]/text()').extract()
        comments = response.xpath('//span[@class="a-size-base review-text review-text-content"]/span/text()').extract()
        review_date = response.xpath('//span[@data-hook="review-date"]/text()').extract()

        for review in zip(reference_id, titles, ratings, comments, review_date): 
            new_review = dict()
            
            rating_str = review[2]
            review_date_str = review[4].split("on", 1)[1].strip()
            
            new_review['reference_id'] = review[0]
            new_review['title'] = review[1]
            new_review['rating'] = float(rating_str.replace(' out of 5 stars', ''))
            new_review['comment'] = review[3]
            new_review['review_date'] = datetime.strptime(review_date_str, '%B %d, %Y')
            
            item['reviews'].append(new_review)
            
        review_urls = response.meta['review_urls']
        
        if not review_urls:
            yield item
        else:
            url = review_urls.pop(0)
            yield scrapy.Request(url, callback=self.parse_review_page, meta={'item': item, 'review_urls': review_urls})
            
    def parse_product_page(self, response):
        asin = response.meta['asin']
        title = response.xpath('//*[@id="productTitle"]/text()').extract_first().strip()
        image = re.search('"large":"(.*?)"',response.text)
        if image is None:
            image = None
        else:
            image = image.groups()[0]
        rating = response.xpath('//*[@id="acrPopover"]/@title').extract_first()
        number_of_reviews = response.xpath('//*[@id="acrCustomerReviewText"]/text()').extract_first()
        price = response.xpath('//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[1]/span[1]/text()').extract_first()

        if not price:
            price = response.xpath('//*[@id="corePrice_feature_div"]/div/span[1]/span[1]/text()').extract_first()

        temp = response.xpath('//*[@id="twister"]')
        sizes = []
        colors = []
        if temp:
            s = re.search('"variationValues" : ({.*})', response.text).groups()[0]
            json_acceptable = s.replace("'", "\"")
            di = json.loads(json_acceptable)
            sizes = di.get('size_name', [])
            colors = di.get('color_name', [])

        bullet_points = response.xpath('//*[@id="feature-bullets"]//li/span/text()').extract()
        seller_rank = response.xpath('//*[text()="Amazon Best Sellers Rank:"]/parent::*//text()[not(parent::style)]').extract()
        
        attributes = []
        attribute_rows = response.xpath('//table[@id="productDetails_detailBullets_sections1"]//tr')
        
        if attribute_rows:
            for row in attribute_rows:
                attribute_item = AttributeItem()
                attribute_item['title'] = row.xpath('.//th/text()').extract_first().strip()
                attribute_item['value'] = row.xpath('.//td/text()').extract_first().strip()
                
                if not attribute_item['title'] or not attribute_item['value']:
                    continue
                
                attributes.append(attribute_item)
        
        item = ProductItem()
        item['site_name'] = "Amazon"
        item['product_identification_number'] = asin
        item['title'] = title
        item['image_src'] = image
        item['rating'] = float(rating.replace(' out of 5 stars', ''))
        item['price'] = float(price.replace('$', ''))
        item['product_url'] = f'https://www.amazon.com/dp/{asin}'
        item['description'] = '\n'.join([i.strip() for i in bullet_points if not i.isspace() and i != '\n' ])
        item['reviews'] = []
        item['attributes'] = attributes
        
        review_urls = []
        
        for i in range(1):
            review_url = f"https://www.amazon.com/product-reviews/{asin}?pageNumber={i+1}"
            review_urls.append(review_url)
        
        review_url = review_urls.pop(0)
        
        yield scrapy.Request(url=review_url, callback=self.parse_review_page, meta={'asin': asin, 'item': item, 'review_urls': review_urls })
    
