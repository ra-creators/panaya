from django.db import models
from product.models import Product
from user_manager.models import UserAddress
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class Order(models.Model):
    # user = models.ForeignKey(User, related_name='order_details', on_delete=models.CASCADE)
    # first_name = models.CharField(max_length=200)
    # last_name = models.CharField(max_length=200)
    # address = models.CharField(max_length=200)
    # postal_code = models.CharField(max_length=6)
    # city = models.CharField(max_length=200)
    address = models.ForeignKey(UserAddress, related_name='order_address',
                                on_delete=models.CASCADE, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    @property
    def total(self):
        total = 0
        for item in self.items.all():
            total = total + item.get_cost()
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def sub_total(self):
        return self.get_cost()

    def get_cost(self):
        return self.price * self.quantity
