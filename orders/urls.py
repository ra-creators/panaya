from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name="order_start"),
    path('address/', views.address, name="order_address"),
    path('add_address/', views.add_address, name="order_add_address"),
    path('order_details/', views.order, name="order_order_details"),
]
