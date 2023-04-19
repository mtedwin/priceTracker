from django_filters import rest_framework as filters
from .models import Product, ProductReview, Site

class SiteFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Site
        fields = ['title']

class ProductReviewFilter(filters.FilterSet):
    num_stars__gte = filters.NumberFilter(field_name='num_stars', lookup_expr='gte')
    num_stars__lte = filters.NumberFilter(field_name='num_stars', lookup_expr='lte')

    class Meta:
        model = ProductReview
        fields = ['num_stars__gte', 'num_stars__lte', 'product']
        
class ProductFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    num_stars__gte = filters.NumberFilter(field_name='num_stars', lookup_expr='gte')
    num_stars__lte = filters.NumberFilter(field_name='num_stars', lookup_expr='lte')
    current_price__gte = filters.NumberFilter(field_name='current_price', lookup_expr='gte')
    current_price__lte = filters.NumberFilter(field_name='current_price', lookup_expr='lte')
    date_retrieved__gte = filters.DateFilter(field_name='date_retrieved', lookup_expr='date__gte')
    date_retrieved__lte = filters.DateFilter(field_name='date_retrieved', lookup_expr='date__lte')
    
    class Meta:
        model = Product
        fields = ['title', 'num_stars__gte', 'num_stars__lte', 'current_price__gte', 'current_price__lte', 'date_retrieved__gte', 'date_retrieved__lte']