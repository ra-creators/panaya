from django.dispatch import receiver
from django.db.models.signals import post_save

# models
from .models import Transaction
# mail utils
from util_mail.views import payment_recieved


@receiver(post_save, sender=Transaction, dispatch_uid="transaction_alert_mail")
def transaction_alert_mail(sender, instance, created, **kwarg):
    if not created:
        return
    payment_recieved(instance)
