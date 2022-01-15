from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:page>/', views.product_list, name='product_list'),

    # categories
    path('categories/', views.categories, name="categories"),
    path('categories/<slug:category_slug>/', views.categories,
         name='product_list_by_category'),
    path('categories/<slug:category_slug>/<int:page>/', views.categories,
         name='product_list_by_category'),
    #     path('categories/<slug:category_slug>/search/', views.categories,
    #     name='product_list_by_category'),


    # collections
    path('collections/', views.collections, name="collections"),
    path('collections/<slug:collection_slug>/', views.collections,
         name='product_list_by_collection'),
    path('collections/<slug:collection_slug>/<int:page>/', views.collections,
         name='product_list_by_collection'),
    #     path('collections/<slug:collection_slug>/search/', views.collections,
    #     name='product_list_by_collection'),


    # types
    path('types/', views.types, name="types"),
    path('types/<slug:type_slug>/', views.types,
         name='product_list_by_type'),
    path('types/<slug:type_slug>/<int:page>/', views.types,
         name='product_list_by_type'),
    #     path('types/<slug:type_slug>/search/', views.types,
    #     name='product_list_by_type'),


    # search
    path('search/', views.product_search, name='product_search'),
    path('search/<int:page>/', views.product_search, name='product_search'),

    # single product
    path('id/<int:id>/', views.product_detail, name='product_detail'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),

    # cart
    path('cart/', views.cart, name="cart"),

    # product feedback
    path('api/product/feedback/', views.feedback_product,
         name='feedback_product')
]
