from django.db import models
from django.core.validators import MinValueValidator
import uuid


class Promotion(models.Model):
    description=models.CharField(max_length=255)
    discount=models.FloatField()


class Collection(models.Model):
    title=models.CharField(max_length=255)
    featured_product=models.ForeignKey('Product',on_delete=models.SET_NULL,null=True,related_name='+')

    def __str__(self):
        return self.title
    
    class Meta:
        ordering=['title']

class Product(models.Model):
    title=models.CharField(max_length=255)
    slug=models.SlugField()
    description=models.TextField()
    unit_price=models.DecimalField(max_digits=6,decimal_places=2)
    inventory=models.IntegerField()
    last_update=models.DateTimeField(auto_now=True)
    collection=models.ForeignKey(Collection,on_delete=models.PROTECT)
    promotions=models.ManyToManyField(Promotion)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering=['title']


class Customer(models.Model):
    MemberSHip_Bronze='B'
    MemberSHip_Silver='S'
    MemberSHip_Gold='G'
    MEMBERSHIP_CHOICES=[
        (MemberSHip_Bronze,'Bronze'),
        (MemberSHip_Silver,'Silver'),
        (MemberSHip_Gold,'Gold')
    ]
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=255)
    birth_date=models.DateField(null=True)
    membership=models.CharField(max_length=1,choices=MEMBERSHIP_CHOICES,default=MemberSHip_Bronze)
    


class Order(models.Model):
    PAYMENT_STATUS=[
        ('P','Pending'),
        ('C','Complete'),
        ('F','Failed')
        ]
    placed_at=models.DateTimeField(auto_now_add=True)
    payment_status=models.CharField(max_length=1, choices=PAYMENT_STATUS, default='P')
    customer=models.ForeignKey(Customer,on_delete=models.PROTECT)

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.PROTECT)
    product=models.ForeignKey(Product,on_delete=models.PROTECT,related_name='orderitems')
    quantity=models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    unit_price=models.DecimalField(max_digits=6,decimal_places=2)


class Adress(models.Model):
    street=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    quantity=models.PositiveIntegerField()
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

    class Meta:
        unique_together=[['cart','product']]

class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    name=models.CharField(max_length=255)
    description=models.TextField()
    date=models.DateField(auto_now_add=True)