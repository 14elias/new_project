from django.contrib import admin
from django.db.models import Count
from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['title','unit_price','inventory_status','collection_title']
    list_per_page=10
    list_select_related=['collection']
    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if product.inventory<10:
            return 'low'
        return 'ok'
    def collection_title(self,product):
        return product.collection.title
    

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display=['title','product_count']

    @admin.display(ordering='product_count')
    def product_count(self,collection):
        return collection.product_count
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(product_count=Count('product'))
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','membership']
    ordering=['first_name','last_name']
    list_editable=['membership']
    list_per_page=10

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['placed_at','payment_status','customer_firstname']
    ordering=['placed_at']
    list_editable=['payment_status']
    list_select_related=['customer']

    def customer_firstname(self,order):
        return order.customer.first_name
