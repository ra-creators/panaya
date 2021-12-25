from django.db import models
import razorpay
from orders.models import Order


class RazorPayOrder(models.Model):
    order = models.OneToOneField(
        Order, related_name='razor_pay_order', on_delete=models.CASCADE
    )
    rp_id = models.CharField(max_length=30, unique=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self) -> str:
        return self.rp_id


class Transaction(models.Model):
    order = models.ForeignKey(
        Order, related_name='transactions', on_delete=models.CASCADE
    )
    razorpay_order = models.ForeignKey(
        RazorPayOrder, related_name='transactions', on_delete=models.CASCADE
    )
    payment_id = models.CharField(max_length=30, )
    payment_sig = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self) -> str:
        return self.payment_id
