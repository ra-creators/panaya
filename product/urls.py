from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('cat/<slug:category_slug>/', views.product_list,
         name='product_list_by_category'),
    path('search', views.product_search, name='product_search'),
    path('search/<int:page>', views.product_search, name='product_search'),
    path('id/<int:id>/', views.product_detail, name='product_detail'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart', views.cart, name="cart")
]
