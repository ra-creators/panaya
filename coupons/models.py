from django.db import models

# Create your models here.
class Coupon(models.Model):
    code = models.CharField(max_length=8, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField()
    percentage = models.BooleanField(default=False)
    active = models.BooleanField()

    def __str__(self):
        return self.code

    class Meta:
        verbose_name_plural = 'Coupons'