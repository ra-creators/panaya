from django.db import models
from product.models import Product
from coupons.models import Coupon
from user_manager.models import UserAddress
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(
        User, related_name='order_details', on_delete=models.CASCADE)
    address = models.ForeignKey(UserAddress, related_name='order_address',
                                on_delete=models.CASCADE, null=False,
                                blank=False)
    coupon = models.ForeignKey(Coupon,
                               related_name='order_coupon',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    razorpay_order_id = models.CharField(
        default='nil', max_length=30, )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return float(total_cost)

    @property
    def name(self):
        return self.__str__()

    @property
    def total(self):
        return float(self.get_total_cost())-float(self.discount)

    def save(self, *args, **kwargs):
        try:
            if(self.coupon):
                # print(self.coupon)
                if(self.coupon.percentage):
                    self.discount = (self.get_total_cost() *
                                     (self.coupon.discount/100))
                else:
                    self.discount = self.coupon.discount
            if self.discount > self.get_total_cost():
                self.discount = self.get_total_cost()

        except Exception as err:
            raise err
        super().save(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        try:
            self.product.update_stocks(self.quantity)
        except Exception as err:
            raise err
        super().save(*args, **kwargs)

class OrderTracking(models.Model):
    """
    Order Tracking Model by storing JSON response
    """
    order = models.OneToOneField(Order,
                              related_name='order_tracking',
                              on_delete=models.CASCADE)
    response = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order Tracking {self.id}"
