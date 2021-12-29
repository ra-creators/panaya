from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string
# from mail import send_mail
from django.core.mail import send_mail as django_send_mail


def send_mail(request, transaction):
    # print("mail send attempt")
    order = transaction.order
    from_email = settings.EMAIL_HOST_USER
    recipient = [order.user.email]
    subject = "Payment for Order #{id} received".format(id=order.id)
    context = {
        'order': order,
        'paid': order.paid,
        'transactions': order.transactions,
        'order_url': request.build_absolute_uri(
            '/orders/order/'+str(order.id)
        ),
    }
    # order_html = render_to_string(
    #     "payment/order_details.html", context=context)
    order_html = render_to_string(
        'payment/order_confirmation.html', context=context)
    order_text = strip_tags(order_html)
    # print(order_text)
    django_send_mail(
        subject=subject,
        message=order_text,
        from_email=from_email,
        html_message=order_html,
        recipient_list=recipient,
    )
    # print("mail send done")


if __name__ == '__main__':
    pass
    # order = Order.objects.get(id=132)
    # send_order_confirmation_mail(order)
