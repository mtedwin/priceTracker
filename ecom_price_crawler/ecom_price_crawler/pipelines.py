# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import datetime
from itemadapter import ItemAdapter
from tracker.models import Product, PriceHistory, Site, ProductReview, Attribute, ProductAttribute

class AmazonPipeline:

    def process_item(self, item, spider):
        
        if not item['price']:
            return item
        
        try:
            product = Product.objects.get(product_identification_number = item['product_identification_number'])
            product.current_price = item['price']
            product.save()
            
            price_history = PriceHistory()
            price_history.price = product.current_price
            price_history.product = product
            price_history.save()
            return item
        except Product.DoesNotExist:
            pass
        
        product = Product()
        product.product_identification_number = item['product_identification_number']
        product.title = item['title']
        product.current_price = item['price']
        product.image_src = item['image_src']
        product.product_url = item['product_url']
        product.num_stars = item['rating']
        product.site = Site.objects.get(title = item['site_name'])
        product.description = item['description']
        product.save()
        
        for product_attribute in item['attributes']:
            attribute, created = Attribute.objects.get_or_create(name=product_attribute['title'])
            obj, created = ProductAttribute.objects.update_or_create(attribute=attribute, product=product, value=product_attribute['value'])
            
        for product_review in item['reviews']:
            obj, created = ProductReview.objects.update_or_create(reference_id=product_review['reference_id'], title=product_review['title'], content=product_review['comment'], num_stars=product_review['rating'], review_date=product_review['review_date'], product=product)
        
        price_history = PriceHistory()
        price_history.price = product.current_price
        price_history.product = product
        price_history.save()
        
        return item