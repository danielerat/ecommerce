from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer,CollectionSerializer
from store.models import Product,Collection
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db.models import Count

@api_view(['GET','POST','DELETE'])
def product_list(request,pk):
    product=Product.objects.select_related("collection").get(pk=pk)
    if request.method == "GET":
        serializer=ProductSerializer(product,context={'request': request})
        return Response(serializer.data)
    elif request.method == "POST":
        serializer=ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        print("-------------------------------")
        collection_id=request.data.get('collection')
        collection=get_object_or_404(Collection,pk=collection_id)
        print(request.data.get('collection'))
        print(serializer.validated_data)
        print("-------------------------------")
        serializer.save(collection=collection)
        return Response("OK")
    elif request.method == "DELETE":
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','PUT'])
def collection_detail(request,pk):
    collection=get_object_or_404(Collection.objects.annotate(products_count=Count('products')),pk=pk)
    if request.method == "GET":
        serializer=CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer=CollectionSerializer(collection,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    