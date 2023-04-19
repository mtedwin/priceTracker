from django.contrib.auth.models import User, Group
from rest_framework import serializers
from tracker.models import Attribute, PriceHistory, Product, ProductAttribute, ProductReview, Site, Attribute
from django.db.models import Avg, Max, Min, FloatField

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
        
class ProductAttributeSerializer(serializers.HyperlinkedModelSerializer):
    attribute_name = serializers.CharField(source="attribute")
    
    def get_attribute_nane(self, obj):
        return obj._attribute.name
    
    class Meta:
        model = ProductAttribute
        fields = '__all__'
        
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        depth = 1
        fields = ['url', 'id', 'title', 'product_url', 'image_src', 'num_stars', 'current_price', 'description', 'site', 'total_average_price', 'max_price_difference', 'product_reviews', 'price_histories', 'product_attributes']
        
    total_average_price = serializers.SerializerMethodField()
    max_price_difference = serializers.SerializerMethodField()
    product_attributes = ProductAttributeSerializer(source="productattribute_set", many=True, read_only=True)
    
    def get_total_average_price(self, obj):
        return obj.price_histories.all().aggregate(Avg('price'))['price__avg']
    
    def get_max_price_difference(self, obj):
        result = obj.price_histories.all().aggregate(max_price_diff=Max('price', output_field=FloatField()) - Min('price', output_field=FloatField()))
        return result.get('max_price_diff')
    
class ProductReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductReview
        fields = ['id', 'title', 'content', 'review_date', 'num_stars', 'product']

class SiteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Site
        fields = ['id', 'title']
        
class PriceHistorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PriceHistory
        fields = ['id', 'price', 'product', 'date_retrieved']
        
class AttributeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'
    