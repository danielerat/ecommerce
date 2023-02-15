from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import ProductSerializer,CollectionSerializer
from store.models import Product,Collection
from django.shortcuts import get_object_or_404
from django.db.models import Count

from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView


#Generic Views

class ProductList(ListCreateAPIView):
    # The Attribute way
    queryset=Product.objects.select_related('collection').all()
    serializer_class=ProductSerializer
    # The bellow is to be used when we want more logic, maybe we want the check 
    # the current user and according to their account perform something
    def get_queryset(self):
        print("----------")
        print(self.request.method)
        print(self.request.query_params)
        print(self.request.user)
        print(self.request.data)
        print(self.request.path)
        print("----------")
        return Product.objects.select_related('collection').all()
    # Maybe we want to return different serializers according to the user, then we should use this way
    def get_serializer_class(self):
        return ProductSerializer
    # We don't have an attribute for specifying the attribute class so either we create our own django or we shush.
    def get_serializer_context(self):
        return {'request': self.request}

# our class based view
# class ProductList(APIView):
#     def get(self,request):
#         product=Product.objects.select_related('collection').all()
#         serializer=ProductSerializer(product,many=True)
#         return Response(serializer.data)
#     def post(self,request):
#         serializer=ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data,status=status.HTTP_201_CREATED)


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    def delete(self,reqeust,pk):
        product=get_object_or_404(Product,pk=pk)
        if product.orderitem_set.count()>0:
             return Response({'error':"Product cannot be deleted because it is associated with an Order"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(ListCreateAPIView):
    queryset=Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class=CollectionSerializer
    

class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset=Collection.objects.annotate(products_count=Count('products'))
    serializer_class=CollectionSerializer
    def delete(self,reqeust,pk):
        # Collection is protected, if a collection has a product, it can not be delete. 
        collection=get_object_or_404(Collection,pk=pk)
        if collection.products.count() > 0:
            return Response({'error':"Collection cannot be deleted because it is associated with a product"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
