from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,ListModelMixin
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CollectionSerializer, ProductSerializer, ReviewSerializer, UpdateCartItemSerializer
from store.models import Cart, CartItem, OrderItem, Product,Collection, Review
from .filter import ProductFilter
from .pagination import DefaultPagination


class ProductViewset(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class=ProductFilter
    pagination_class=DefaultPagination
    search_fields=['title','description']
    ordering_fields=['unit_price','last_update']



    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk'].count()>0):
            return Response({"you can't delete it because it is ordered"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
    
    
class CollectionViewset(ModelViewSet):
    queryset=Collection.objects.all()
    serializer_class=CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk'].count()>0):
            return Response({'you can not delete it '},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
        
class ReviewViewset(ModelViewSet):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer

class CartViewset(DestroyModelMixin,RetrieveModelMixin,CreateModelMixin,GenericViewSet):
    serializer_class=CartSerializer
    queryset=Cart.objects.prefetch_related('items__product').all()

class CartItemViewset(ModelViewSet):
    http_method_names=['get','post','patch','delete']
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.method=='POST':
            return AddCartItemSerializer
        elif self.request.method=='PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}