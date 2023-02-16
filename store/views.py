from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import ProductSerializer,CollectionSerializer,ReviewSerializer
from store.models import Product,Collection,OrderItem,Review
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView

from rest_framework.viewsets import ModelViewSet

# ViewSet(which is simply a combination of a bunch of generic Views with more things )
class ProductViewSet(ModelViewSet):
    
    serializer_class=ProductSerializer
    def get_serializer_context(self):
        return {'request': self.request}
    
    def get_queryset(self):
        queryset=Product.objects.all()
        collection_id=self.request.query_params.get("collection_id")
        if collection_id is not None:
            queryset=queryset.filter(collection_id=collection_id)
            
        return queryset

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
    


class ReviewViewset(ModelViewSet):
    
    serializer_class=ReviewSerializer
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}