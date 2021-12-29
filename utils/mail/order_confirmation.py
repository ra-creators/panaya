from django.template.loader import render_to_string, get_template
from django.template import Context
from django.utils.html import strip_tags
from django.conf import settings
# from mail import send_mail
from django.core.mail import send_mail


def send_order_confirmation_mail(request, order):
    # print("mail send attempt")
    from_email = settings.EMAIL_HOST_USER
    recipient = [order.user.email]
    subject = "Order #{id} placed".format(id=order.id)
    context = {
        'order': order,
        'paid': order.paid,
        'transactions': order.transactions,
        'order_url': request.build_absolute_uri('/orders/order/'+str(order.id)),
    }
    # order_html = render_to_string(
    #     "payment/order_details.html", context=context)
    order_text = render_to_string(
        'payment/order_confirmation.html', context=context)
    # print(order_text)
    send_mail(subject=subject, message=order_text, from_email=from_email, html_message=order_text,
              recipient_list=recipient, )
    # print("mail send done")


if __name__ == '__main__':
    pass
    # order = Order.objects.get(id=132)
    # send_order_confirmation_mail(order)
