from django.shortcuts import get_object_or_404
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.decorators import action
from store.permissions import IsAdminOrReadOnly,ViewCustomerHistoryPermission
from store.serializers import AddCartItemSerializer, CreateOrderSerializer, OrderSerializer, ProductImageSerializer, ProductSerializer,CollectionSerializer,ReviewSerializer, CartItemSerializer, CartSerializer, UpdateCartItemSerializer,CustomerSerializer, UpdateOrderSerializer
from store.models import Order, Product,Collection,OrderItem, ProductImage,Review,Cart, CartItem,Customer
from store.filters import ProductFilter
from store.pagination import DefaultPagination
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.mixins import DestroyModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin

# ViewSet(which is simply a combination of a bunch of generic Views with more things )
class ProductViewSet(ModelViewSet):
    queryset=Product.objects.prefetch_related('images').all()
    serializer_class=ProductSerializer
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class=ProductFilter
    pagination_class=DefaultPagination
    permission_classes=[IsAdminOrReadOnly]
    search_fields=['title','description','collection__title']
    ordering_fields=['unit_price','last_update']
    def get_serializer_context(self):
        return {'request': self.request}
    
    

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']):
             return Response({'error':"Product cannot be deleted because it is associated with an Order"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    

class CollectionViewSet(ModelViewSet):
    queryset=Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class=CollectionSerializer
    permission_classes=[IsAdminOrReadOnly]

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

class CartViewset(DestroyModelMixin,RetrieveModelMixin,CreateModelMixin,GenericViewSet):
    queryset=Cart.objects.prefetch_related('items__product').all()
    serializer_class=CartSerializer

class CartItemViewset(ModelViewSet):
    http_method_names=['get','post','patch','delete']
    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart_id=self.kwargs['cart_pk'])
    def get_serializer_class(self):
            if self.request.method == 'POST':
                return AddCartItemSerializer
            if self.request.method == 'PATCH':
                return UpdateCartItemSerializer
            return CartItemSerializer
    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}


class CustomerViewset(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class=CustomerSerializer
    permission_classes=[IsAdminUser]

    @action(detail=True,permission_classes=[ViewCustomerHistoryPermission])
    def history(self,request,pk):
        return Response('ok')

    
    @action(detail=False,methods=['GET','PUT'],permission_classes=[IsAuthenticated])
    def me(self,request):
        customer=Customer.objects.get(user_id=request.user.id)
        if request.method=='GET':
            serializer=CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer=CustomerSerializer(customer,data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data)

class OrderViewset(ModelViewSet):
    http_method_names=['get', 'patch', 'post','delete','head', 'options']
    permission_classes=[IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
            # Admin should delete and update 
            return [IsAdminUser()]
            # Authenticated users should view only
        return [IsAuthenticated()]
    def create(self, request, *args, **kwargs):
        serializer=CreateOrderSerializer(data=request.data,context={'user_id':self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order=serializer.save()
        serializer=OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer 

    def get_queryset(self):
        # Is user is staff, then, get all orders, otherwise, get his orders only 
        user=self.request.user
        if user.is_staff:
            return Order.objects.prefetch_related("items__product").all()
        (customer_id)=Customer.objects.only('id').get(user_id=user.id)
        return Order.objects.prefetch_related("items__product").filter(customer_id=customer_id)

 
class ProductImageViewset(ModelViewSet):
    serializer_class=ProductImageSerializer

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])
    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}