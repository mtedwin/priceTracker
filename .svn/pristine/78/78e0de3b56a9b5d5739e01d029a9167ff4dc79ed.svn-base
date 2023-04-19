from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from tracker import views

defaultRouter = routers.DefaultRouter()
defaultRouter.register(r'users', views.UserViewSet)
defaultRouter.register(r'groups', views.GroupViewSet)
defaultRouter.register(r'products', views.ProductViewSet)
defaultRouter.register(r'reviews', views.ProductReviewViewSet)
defaultRouter.register(r'sites', views.SiteViewSet)
defaultRouter.register(r'product_price_histories', views.PriceHistoryViewSet)
defaultRouter.register(r'product_attributes', views.ProductAttributeViewSet)
defaultRouter.register(r'attributes', views.AttributeViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(defaultRouter.urls)),
    path('api/me', views.Profile.as_view(), name="me"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]