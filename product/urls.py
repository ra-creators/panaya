from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),

    # categories
    path('categories/', views.categories, name="categories"),
    path('categories/<slug:category_slug>/', views.categories,
         name='product_list_by_category'),

    # collections
    path('collections/', views.collections, name="collections"),
    path('collections/<slug:collection_slug>/', views.collections,
         name='product_list_by_collection'),

    # search
    path('search', views.product_search, name='product_search'),
    path('search/<int:page>', views.product_search, name='product_search'),

    # single product
    path('id/<int:id>/', views.product_detail, name='product_detail'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),

    # cart
    path('cart', views.cart, name="cart"),
]
