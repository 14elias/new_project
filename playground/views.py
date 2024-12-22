from django.shortcuts import render
from django.db.models.aggregates import Max,Min,Avg,Count
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from store.models import Product,OrderItem,Order
from tags.models import *
def hello(request):
    queryset=TaggedItem.objects.get_tags_for(Product,1)
    return render(request,'playground/hello.html', {'result':list(queryset)})