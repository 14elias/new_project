from django.contrib import admin
from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['title','unit_price','inventory_status']
    list_per_page=10
    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if product.inventory<10:
            return 'low'
        return 'ok'

admin.site.register(Collection)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','membership']
    ordering=['first_name','last_name']
    list_editable=['membership']
    list_per_page=10