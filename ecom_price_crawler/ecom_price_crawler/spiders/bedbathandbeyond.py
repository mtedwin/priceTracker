import os
import scrapy
from urllib.parse import urlencode, urljoin
from ecom_price_crawler.items import ProductItem, AttributeItem
from datetime import datetime

class BedBathAndBeyondScraper(scrapy.Spider):
    name="bedbathandbeyond"
    allowed_domains = ['https://www.bedbathandbeyond.com', 'bedbathandbeyond.com']
    start_urls = ['https://www.bedbathandbeyond.com/']
    os.environ["http_proxy"] = "http://185.199.231.45:8382"
    
    def start_requests(self):
        url = 'https://www.bedbathandbeyond.com/apis/services/composite/product-listing/v1.0/all?site=BedBathUS&currencyCode=USD&country=US&rT=xtCompat&tz=-480&categoryId=16066&categoryType=plp_l3&countOnly=false&displayAdsAt=6&higherShippingThreshhold=0.1&pageURI=%2Fstore%2Fcategory%2Fbedding%2Fpillows%2Fbed-pillows%2F16066&solrCat=true&view=grid&web3feo=true&piqIndex=12&slot=15015&noFacet=false&facets=%7B%7D&start=0&perPage=86&sws=&storeOnlyProducts=false&storeId=1&customPriceRange=false&__amp_source_origin=https%3A%2F%2Fwww.bedbathandbeyond.com'
        yield scrapy.Request(url=url, callback=self.parse_search_response)
    
    def parse_search_response(self, response):
        json_response = response.json()
        for doc in json_response['response']['docs']:
            product_id = doc['PRODUCT_ID']
            product_url = f"https://www.bedbathandbeyond.com/apis/services/composite/v1.0/pdp-details/{product_id}?&siteId=BedBathUS&skuId=&color=&size=&bopisStoreId=&pickup=&sdd=&tz=-480&allSkus=true&ssr=true&__amp_source_origin=https%3A%2F%2Fwww.bedbathandbeyond.com"
            yield scrapy.Request(url=product_url, callback=self.parse_product_details, meta={'product_id': product_id })
             
    def parse_product_details(self, response):
        product_id = response.meta['product_id']
        json_response = response.json()
        details = json_response['data']['PRODUCT_DETAILS']
        
        default_image_id = details['PRODUCT_IMG_ARRAY'][0]['imageId']
        product_relative_url = details['PDP_URL']
        
        attributes = []
        
        for feature in details['FEATURES']:
            for key, value in feature.items():
                attribute_item = AttributeItem()
                attribute_item["title"] = key
                attribute_item["value"] = value
                attributes.append(attribute_item)
                
        item = ProductItem()
        item['site_name'] = "Bed Bath & Beyond"
        item['product_identification_number'] = details['SKU_ID']
        item['title'] = details['DISPLAY_NAME']
        item['image_src'] = f'https://b3h2.scene7.com/is/image/BedBathandBeyond/{default_image_id}'
        item['price'] = float(details['IS_PRICE'].replace('$', ''))
        item['rating'] = details['RATINGS']
        item['product_url'] = f'https://www.bedbathandbeyond.com{product_relative_url}'
        item['description'] = details['LONG_DESCRIPTION']
        item['reviews'] = []
        item['attributes'] = attributes
        
        review_url = f"https://www.bedbathandbeyond.com/apis/services/conversations/review?ProductId={product_id}&Stats=Reviews&sort=SubmissionTime+desc&start=0&rows=20&photoRows=8&photoStart=0&photo=true&isBrowser=true&collectionFlag=false&__amp_source_origin=https://www.bedbathandbeyond.com"
        yield scrapy.Request(url=review_url, callback=self.parse_product_reviews, meta={'product_id': product_id, 'item': item})        
        
    def parse_product_reviews(self, response):
        item = response.meta['item']
        
        json_response = response.json()
        
        for result in json_response['Results']:
            new_review = dict()
            
            submission_time_str = result['SubmissionTime']
            submission_time = datetime.fromisoformat(submission_time_str)
            
            new_review['reference_id'] = result['id']
            new_review['title'] = result['Title']
            new_review['rating'] = result['Rating']
            new_review['comment'] = result['ReviewText']
            new_review['review_date'] = submission_time
            
            item['reviews'].append(new_review)

        yield item