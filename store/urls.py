from django.urls import path,include
from rest_framework_nested import routers
from . import views

# Initialize the simple router, to use with Viewset
router=routers.DefaultRouter()

# Line Bellow Generate two urls, 
# -> products(with the name 'product-list') 
# -> products/<pk>(with the name 'product-detail').
router.register('products',views.ProductViewSet,basename='products') 
# Same for the Collection.
router.register('collections',views.CollectionViewSet)
router.register('carts',views.CartViewset)
router.register('customers',views.CustomerViewset)
router.register('orders',views.OrderViewset,basename="orders")


# Creating a nested router (list:products/2/reviews and detail:products/2/reviews/1)
# Three arguments need to be passed, "Parent Router(which is router)" , Parent prefix(which is product) and lookup parameter
products_router=routers.NestedSimpleRouter(router,'products',lookup='product')
# base name helps us to have (product-reviews-list and product-reviews-detail views of our view set)
products_router.register('reviews',views.ReviewViewset,basename='product-reviews')
products_router.register('images',views.ProductImageViewset,basename='product-images')

carts_router=routers.NestedSimpleRouter(router,'carts',lookup='cart')
carts_router.register('items',views.CartItemViewset,basename='cart-items')

urlpatterns = [
  path('',include(router.urls)),
  path('',include(products_router.urls)),
  path('',include(carts_router.urls)),
]