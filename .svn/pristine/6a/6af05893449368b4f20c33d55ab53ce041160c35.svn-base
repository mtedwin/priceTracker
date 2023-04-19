from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Site(models.Model):
    title = models.CharField(max_length=500)
    
    def __str__(self):
        return self.title
    
class Attribute(models.Model):
    name = models.CharField(max_length=1000)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    title = models.CharField(max_length=500)
    product_identification_number = models.CharField(max_length=500)
    current_price = models.FloatField(max_length=30)
    product_url = models.URLField(max_length=1000)
    image_src = models.URLField(max_length=1000)
    num_stars = models.FloatField(max_length=30)
    description = models.CharField(max_length=4000, blank=True, null=True)
    date_retrieved = models.DateTimeField(default=timezone.now)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    attributes = models.ManyToManyField(Attribute, through='ProductAttribute')
    
    def __str__(self):
        return self.title
    
class ProductReview(models.Model):
    title = models.CharField(max_length=1000)
    content = models.CharField(max_length=2000)
    reference_id = models.CharField(max_length=500)
    review_date = models.DateField(blank=True, null=True)
    num_stars = models.FloatField(max_length=30, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_reviews')
    
class PriceHistory(models.Model):
    price = models.FloatField(max_length=30)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_histories')
    date_retrieved = models.DateTimeField(default=timezone.now)
    
class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=1000)