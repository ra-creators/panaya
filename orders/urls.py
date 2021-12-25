from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_order, name="create_order"),
    path('buy/<int:product_id>', views.buy_now, name="buy_now"),

    path('order/<int:order_id>', views.order_details, name="order_details"),
]
