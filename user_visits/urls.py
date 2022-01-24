from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('homecount/', views.increase_home_count, name='increase_home_count'),
    path('cartcount/', views.increase_cart_count, name='increase_cart_count'),
    path('blogcount/', views.increase_blog_count, name='increase_blog_count'),

]