from django.contrib import admin, messages
from django.db import models
from django.forms import CheckboxSelectMultiple
from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from .models import (Category, Product, Tag, ProductImage, Review, FAQ,
                     Collection, Type, Color)

import io
import csv
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0


class ReviewInLine(admin.StackedInline):
    model = Review
    extra = 0


class FaqInLine(admin.StackedInline):
    model = FAQ
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['inventory_id', 'name', 'price',
                    'stocks', 'available', 'updated', ]
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ReviewInLine, FaqInLine]

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    def bulk_import(self, request, queryset=None):
        # print('hei')
        # print(request, request.POST)
        context = {
            'queryset': queryset,
            'action_name': 'bulk_import',
        }
        if 'do_action' in request.POST:
            # print(request.POST)
            # print(request.FILES)
            if 'fileInput' not in request.FILES:
                # return HttpResponseRedirect()
                msg = (
                    'failed to complete action : no import file')
                self.message_user(
                    request, message=msg, level=messages.ERROR)
                return redirect('admin:product_product_changelist')
            try:
                paramFile = io.TextIOWrapper(request.FILES['fileInput'].file)
                csv_data = list(csv.DictReader(paramFile))
            except Exception as err:
                msg = (
                    'failed to complete action #CSV_FILE : ', err)
                self.message_user(
                    request, message=msg, level=messages.ERROR)
                return redirect('admin:product_product_changelist')
            try:
                objs_create = []
                objs_update = []
                editable_fields = [
                    'name', 'description', 'price', 'stocks',
                    'category_id', 'collection_id', 'type_id', 'slug']
                for row in csv_data:
                    if Product.objects.filter(inventory_id=row['id']).exists():
                        obj = Product.objects.get(inventory_id=row['id'])
                        for editable_field in editable_fields:
                            if editable_field == 'slug':
                                obj.slug = slugify(obj.name)
                                continue
                            if editable_field in row and row[editable_field]:
                                setattr(obj, editable_field,
                                        row[editable_field])
                        objs_update.append(obj)
                    else:
                        obj = Product(
                            inventory_id=row['id'],
                            slug=slugify(row['name']),
                            name=row['name'],
                            description=row['description'],
                            price=row['price'],
                            stocks=row['stocks'],
                            category_id=row['category_id'],
                            collection_id=row['collection_id'],
                            type_id=row['type_id'],
                        )
                        objs_create.append(obj)
            except Exception as err:
                # print(err)
                msg = (
                    'failed to complete action #DATA_FORMAT : ', err)
                self.message_user(
                    request, message=msg, level=messages.ERROR)

                return redirect('admin:product_product_changelist')

            try:
                Product.objects.bulk_create(objs_create, )
                Product.objects.bulk_update(
                    objs_update, fields=editable_fields)
            except Exception as err:
                msg = (
                    'failed to complete action #CRETE_UPDATE: ', err)
                self.message_user(
                    request, message=msg, level=messages.ERROR)
                return redirect('admin:product_product_changelist')

            msg = (
                "Succesfully added {no_created} products, update {no_update}"
                .format(
                    no_created=len(objs_create),
                    no_update=len(objs_update)
                )
            )
            self.message_user(
                request, message=msg, level=messages.INFO)
            return redirect('admin:product_product_changelist')
        return render(request, 'admin/bulk_update.html', context=context)

    actions = [bulk_import, ]
    noqueryst_actions = ['bulk_import', ]

    def changelist_view(self, request, extra_context=None):
        if ('action' in request.POST and
                request.POST['action'] in self.noqueryst_actions):
            # print(request.POST)
            if not request.POST.getlist('_selected_action'):
                post = request.POST.copy()
                for u in Product.objects.all():
                    post.update({'_selected_action': str(u.id)})
                    break
                request._set_post(post)
        return super(ProductAdmin, self).changelist_view(request,
                                                         extra_context)


@ admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@ admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question']


@ admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['stars']
    # list_filter = ['product', 'created']


admin.site.register(Color, admin.ModelAdmin)
