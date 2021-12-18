from django.contrib import admin
from django.db.models.base import Model
from .models import Category, Product, Tag, ProductImage, Review, FAQ

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0

class ReviewInLine(admin.StackedInline):
    model = Review
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stocks', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ReviewInLine]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image']
    list_filter = ['product']

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question']

    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['stars']
    # list_filter = ['product', 'created']