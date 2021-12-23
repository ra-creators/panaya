from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start, name="order_start"),
    path('order/<int:order_id>', views.order_details, name="order_details"),
    path('address/', views.address, name="order_address"),
    path('add_address/', views.add_address, name="order_add_address"),
    path('verify_order/', views.verify_order, name="order_verify_details"),
    path('create_order/', views.create_order, name="order_create"),
]
