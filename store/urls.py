from django.urls import path
from . import views

urlpatterns = [
    path("products/<int:pk>",views.product_list),
    path('collections/<int:pk>',views.collection_detail,name='collection-detail')
]