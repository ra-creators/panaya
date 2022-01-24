from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(HomeCount)
class HomeCountAdmin(admin.ModelAdmin):
    list_display = ['count', 'created']

@admin.register(CartCount)
class CartCountAdmin(admin.ModelAdmin):
    list_display = ['count', 'created']
    
@admin.register(BlogCount)
class BlogCountAdmin(admin.ModelAdmin):
    list_display = ['count', 'created']
