from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from .models import HomeCount, CartCount, BlogCount
# Create your views here.

def increase_home_count(request):
    try:
        obj = HomeCount.objects.get(created__day=datetime.now().day)
        obj.increase_count()    
    except:
        HomeCount.objects.create(count=1, created=datetime.now())
    return HttpResponse(f"ok")

def increase_blog_count(request):
    try:
        obj = BlogCount.objects.get(created__day=datetime.now().day)
        obj.increase_count()    
    except:
        BlogCount.objects.create(count=1, created=datetime.now())
    return HttpResponse(f"ok")

def increase_cart_count(request):
    try:
        obj = CartCount.objects.get(created__day=datetime.now().day)
        obj.increase_count()    
    except:
        CartCount.objects.create(count=1, created=datetime.now())
    return HttpResponse(f"ok")
