from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import OTP, UserAddress, ConnectEmails
from orders.models import Order
User = get_user_model()


class OrderInline(admin.TabularInline):
    model = Order
    can_delete = False
    extra = 0
    show_change_link = True
    fields = ['updated', 'total']
    readonly_fields = ['updated', 'total', 'address', ]

    def has_add_permission(self, request, obj):
        return False


class UserAddressInline(admin.StackedInline):
    model = UserAddress
    can_delete = False
    extra = 0
    verbose_name_plural = 'UserAddress'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (UserAddressInline, OrderInline)


admin.site.register(OTP)
admin.site.register(ConnectEmails)