from rest_framework import serializers
from .models import Collection,Product

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields=["id","title","products_count"]
    products_count=serializers.IntegerField(read_only=True)
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields= ["id", "title","slug","description","inventory","last_update", "unit_price","collection"]

