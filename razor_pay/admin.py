from django.contrib import admin
from .models import Transaction, RazorPayOrder


admin.site.register(RazorPayOrder)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'timestamp', 'order']
    exclude = ['razorpay_order', 'payment_sig']
    readonly_fields = ['payment_id', 'order', 'timestamp']
