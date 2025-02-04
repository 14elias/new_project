from django.contrib import admin
from django.db.models import Count
from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['title','unit_price','inventory_status','collection_title']
    list_per_page=10
    list_select_related=['collection']
    list_filter=['collection','last_update']
    search_fields=['title__istartswith']
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
    search_fields=['first_name__istartswith','last_name__istartswith']
    
class OrderItemInline(admin.TabularInline):
    model=OrderItem
    autocomplete_fields=['product']
    extra=0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['placed_at','payment_status','customer_firstname']
    ordering=['placed_at']
    inlines=[OrderItemInline]
    list_editable=['payment_status']
    list_select_related=['customer']
    list_per_page=10
   

    def customer_firstname(self,order):
        return order.customer.first_name

from django.contrib import admin
from .models import Cart


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Filter only valid UUIDs
        return queryset.extra(where=["CHAR_LENGTH(id) = 36"])

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)

