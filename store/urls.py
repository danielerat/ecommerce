from django.urls import path,include
from rest_framework.routers import SimpleRouter
from . import views

# Initialize the simple router, to use with Viewset
router=SimpleRouter()

# Line Bellow Generate two urls, 
# -> products(with the name 'product-list') 
# -> products/<pk>(with the name 'product-detail').
router.register('products',views.ProductViewSet) 
# Same for the Collection.
router.register('collections',views.CollectionViewSet)

urlpatterns = [
  path('',include(router.urls)),
]