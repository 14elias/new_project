from rest_framework import serializers
from decimal import Decimal
from django.db.models.aggregates import Count
from django.db import transaction
from store.models import Cart, CartItem, Customer, OrderItem, Product,Collection, Review,Order

class CollectionBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields=['id','title','featured_product']
class ProductSerializer(serializers.ModelSerializer):
    collection=CollectionBaseSerializer()
    class Meta:
        model=Product
        fields=['id','slug','title','description','unit_price','inventory','collection','price_tax']

    price_tax=serializers.SerializerMethodField(method_name='calculate_tax')   
    def calculate_tax(self,product:Product):
        return product.unit_price*Decimal(0.1)
    

class CollectionSerializer(serializers.ModelSerializer):
    products_count=serializers.SerializerMethodField(method_name='count_product')
    class Meta:
        model=Collection
        fields=['id','title','products_count']
        read_only_fields=['products_count']
    
    def count_product(self,collection:Collection):
        return collection.product_set.count()

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=['id','name','description','product']

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','unit_price']

class CartItemSerializer(serializers.ModelSerializer):
    product=SimpleProductSerializer()
    total_price=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=CartItem
        fields=['id','quantity','cart','product','total_price']

    def get_total_price(self,obj):
        return obj.product.unit_price * obj.quantity

class CartSerializer(serializers.ModelSerializer):
    id=serializers.UUIDField(read_only=True)
    items=CartItemSerializer(many=True,read_only=True)
    total_price=serializers.SerializerMethodField(read_only=True)

    def get_total_price(self,cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])
    class Meta:
        model=Cart
        fields=['id','items','total_price']

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id=serializers.IntegerField()
    def validate_product_id(self,value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError ('no product with the given id was found')
        return value
    def save(self, **kwargs):
        cart_id=self.context['cart_id']
        product_id=self.validated_data['product_id']
        quantity=self.validated_data['quantity']

        try:
            cart_item=CartItem.objects.get(cart_id=cart_id,product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance=cart_item
        except CartItem.DoesNotExist:
            self.instance=CartItem.objects.create(cart_id=cart_id,**self.validated_data)
        return self.instance
    class Meta:
        model=CartItem
        fields=['id','product_id','quantity']

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['quantity']

class CustomerSerializer(serializers.ModelSerializer):
    user_id=serializers.IntegerField(read_only=True)
    class Meta:
        model=Customer
        fields=['id','phone','birth_date','membership','user_id']

class OrderItemSerializer(serializers.ModelSerializer):
    product=SimpleProductSerializer()
    class Meta:
        model=OrderItem
        fields=['id','order','product','quantity','unit_price']
class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True)
    class Meta:
        model=Order
        fields=['placed_at','payment_status','customer','items']

class CreateOrderSerializer(serializers.Serializer):
    with transaction.atomic():
        cart_id=serializers.UUIDField()

        def save(self,**kwargs):
            # print(self.context['user_id'])
            # print(self.validated_data['cart_id'])
            cart_items=CartItem.objects.\
                    select_related('product').\
                    filter(cart_id=self.validated_data['cart_id'])
            
            (customer,created)=Customer.objects.get_or_create(user_id=self.context['user_id'])
            order=Order.objects.create(customer=customer)
            order_items=[
                OrderItem(
                    order=order,
                    product=item.product,
                    unit_price=item.product.unit_price,
                    quantity=item.quantity
                ) for item in cart_items
            ]
            Order.objects.bulk_create(order_items)
            Cart.objects.filter(pk=self.validated_data['cart_id']).delete()

            return order