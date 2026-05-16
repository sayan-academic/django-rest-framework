from django.urls import path, include
# from .views import ProductGetPostGenericAPIview, ProductGetPutDeleteGenericAPIview, ReviewGetPostGenericAPIview, ReviewGetPutDeleteGenericAPIview
from .views import ProductModelViewSet, ReviewModelViewSet
from rest_framework import routers


#strictly for viewsets
'''
product_list = ProductModelViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
product_detail = ProductModelViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
review_list = ReviewModelViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
review_detail = ReviewModelViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
'''
'''
    #products endpoints
    path('products/', product_list, name='product-list'),
    path('products/<int:pk>/', product_detail, name='product-detail'),

    #reviews endpoints
    path('reviews/', review_list, name='review-list'),
    path('reviews/<int:pk>/', review_detail, name='review-detail'),
'''

router = routers.SimpleRouter()
router.register(r'products', ProductModelViewSet)
router.register(r'reviews', ReviewModelViewSet)

urlpatterns = [
   
]
urlpatterns += router.urls