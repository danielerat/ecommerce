from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import ProductSerializer,CollectionSerializer
from store.models import Product,Collection
from django.shortcuts import get_object_or_404
from django.db.models import Count

# our class based view
class ProductList(APIView):
    def get(self,request):
        product=Product.objects.select_related('collection').all()
        serializer=ProductSerializer(product,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
class ProductDetail(APIView):
    def get(self,request,pk):
        product=Product.objects.select_related('collection').get(pk=pk)
        serializer=ProductSerializer(product)
        return Response(serializer.data)
    def put(sef,request,pk):
        product=Product.objects.select_related('collection').get(pk=pk)
        serializer=ProductSerializer(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def delete(self,reqeust,pk):
        product=Product.objects.select_related('collection').get(pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(APIView):
    def get(self,reqeust):
        collection=Collection.objects.annotate(products_count=Count('products')).all()
        serializer=CollectionSerializer(collection,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

class CollectionDetail(APIView):
    def get(self,reqeust,pk):
        collection=Collection.objects.annotate(products_count=Count('products')).get(pk=pk)
        serializer=CollectionSerializer(collection)
        return Response(serializer.data)
    def put(self,request,pk):
        collection=Collection.objects.annotate(products_count=Count('products')).get(pk=pk)
        serializer=CollectionSerializer(collection,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def delete(self,reqeust,pk):
        collection=Collection.objects.get(pk=pk)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
