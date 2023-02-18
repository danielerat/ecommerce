from rest_framework import serializers
from .models import Cart, CartItem, Collection, Order, OrderItem,Product,Review,Customer

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields=["id","title","products_count"]
    products_count=serializers.IntegerField(read_only=True)

# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields= ["id", "title","slug","description","inventory","last_update", "unit_price","collection"]

# Serializer to view a simplified version of product
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields= ["id", "title","unit_price"]


# Review serializer
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=['id','date','name','description']

    def create(self, validated_data):
        product_id=self.context['product_id']
        return Review.objects.create(product_id=product_id,**validated_data)



# Cart Item Serializer
class CartItemSerializer(serializers.ModelSerializer):
    product=SimpleProductSerializer()
    total_price=serializers.SerializerMethodField()
    class Meta:
        model=CartItem
        fields=['id','product','quantity',"total_price"]
    
    def get_total_price(self,cart_item):
        return cart_item.product.unit_price * cart_item.quantity 
    
# Serializers for carts 
class CartSerializer(serializers.ModelSerializer):
    id=serializers.UUIDField(read_only=True)
    items=CartItemSerializer(many=True,read_only=True)
    total_price=serializers.SerializerMethodField()
    class Meta:
        model=Cart
        fields=['id','items','total_price']
    def get_total_price(self,cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

# Serializer to be used when adding an item to a cart
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id=serializers.IntegerField()
    class Meta:
        model=CartItem
        fields=['id','product_id','quantity']
    # Validate a single field(product_id) to make sure it exists.
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("No product with the given id was found")
        return value

    def save(self, **kwargs):
        cart_id=self.context['cart_id']
        product_id=self.validated_data['product_id']
        quantity=self.validated_data['quantity']
        # get the cart
        try:
            # We have a cart item, Update it.
            cart_item=CartItem.objects.get(cart_id=cart_id,product_id=product_id)
            cart_item.quantity=quantity
            cart_item.save()
            self.instance=cart_item
        except CartItem.DoesNotExist:
            # We don't have the cart item, create it. 
           self.instance= CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        return self.instance
     

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['quantity']


class CustomerSerializer(serializers.ModelSerializer):
    user_id=serializers.IntegerField(read_only=True)
    class Meta:
        model=Customer
        fields=['id','user_id','birth_date','membership']



class orderItemSerializer(serializers.ModelSerializer):
    product=SimpleProductSerializer()
    class Meta:
        model=OrderItem
        fields=['id','product','quantity','unit_price']

class OrderSerializer(serializers.ModelSerializer):
    items=orderItemSerializer(many=True)
    class Meta:
        model=Order
        fields=['id','customer','placed_at','payment_status','items']