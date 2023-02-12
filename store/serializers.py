from rest_framework import serializers
from .models import Collection,Product

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields=["id","title","products_count"]
    products_count=serializers.IntegerField()
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields= ["id", "title","slug","description","inventory","last_update", "unit_price","collection"]
    # collection =CollectionSerializer(read_only=True)
    
    # def create(self,validated_data):
    #     print("-------------------------------")
    #     print(validated_data)
    #     print("-------------------------------")
    #     product=Product(**validated_data)
    #     product.collection=Collection.objects.get(pk=3)
    #     product.save()
    #     return product
        