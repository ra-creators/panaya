from django.db import models
from product.models import Product
from coupons.models import Coupon
from user_manager.models import UserAddress
from django.contrib.auth import get_user_model

User = get_user_model()


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
    razorpay_invoice_id = models.CharField(
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
        return float(self.get_total_cost())-float(self.discount_amount)

    @property
    def discount_amount(self):
        discount_amaount = 0
        if(self.coupon):
            if(self.coupon.percentage):
                discount_amaount = (self.get_total_cost() *
                                    (self.coupon.discount/100))
            else:
                discount_amaount = self.coupon.discount
        if discount_amaount > self.get_total_cost():
            discount_amaount = self.get_total_cost()
        return discount_amaount

    def save(self, *args, **kwargs):
        for order_item in self.items.all():
            try:
                order_item.product.update_stocks(order_item.quantity)
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


class OrderTracking(models.Model):
    """
    Order Tracking Model by storing JSON response
    """
    order = models.OneToOneField(Order,
                                 related_name='order_tracking',
                                 on_delete=models.CASCADE)
    shiprocket_order_id = models.CharField(max_length=20)
    shiprocket_shipment_id = models.CharField(max_length=20)
    delivered = models.BooleanField(default=False)
    response = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order Tracking {self.id}"


class ShipRocketToken(models.Model):
    token = models.CharField(max_length=300)
    created_at = models.DateTimeField()
