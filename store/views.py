from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import ProductSerializer,CollectionSerializer
from store.models import Product,Collection,OrderItem
from django.shortcuts import get_object_or_404
from django.db.models import Count

from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView

from rest_framework.viewsets import ModelViewSet

# ViewSet(which is simply a combination of a bunch of generic Views with more things )
class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']):
             return Response({'error':"Product cannot be deleted because it is associated with an Order"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    

class CollectionViewSet(ModelViewSet):
    queryset=Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class=CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']):
             return Response({'error':"Collection cannot be deleted because it is associated with a product"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    


