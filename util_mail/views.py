from orders.models import Order
from django.conf import settings
from django.shortcuts import render
from django.utils.html import strip_tags
from django.template.loader import render_to_string

# python modules
import threading
# from mail import send_mail
from django.core.mail import send_mail as django_send_mail


default_mail = settings.EMAIL_HOST_USER


def generic(recipient, subject, text_content,
            html_content=None, from_email=default_mail, ):
    if html_content:
        django_send_mail(
            subject=subject,
            message=text_content,
            from_email=from_email,
            recipient_list=recipient,
            html_message=html_content,
        )
    else:
        django_send_mail(
            subject=subject,
            from_email=from_email,
            message=text_content,
            recipient_list=recipient,
        )


class EmailThread(threading.Thread):
    def __init__(self, recipient, subject, text_content,
                 html_content=None, from_email=default_mail,):
        self.subject = subject
        self.from_email = from_email
        self.recipient = recipient
        self.text_content = text_content
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        if self.html_content:
            django_send_mail(
                subject=self.subject,
                message=self.text_content,
                from_email=self.from_email,
                recipient_list=self.recipient,
                html_message=self.html_content,
            )
        else:
            django_send_mail(
                subject=self.subject,
                from_email=self.from_email,
                message=self.text_content,
                recipient_list=self.recipient,
            )


def order_confirmation(request, order):
    # print("mail send attempt")
    from_email = settings.EMAIL_HOST_USER
    recipient = [order.user.email]
    subject = "Order #{id} placed".format(id=order.id)
    context = {
        'order': order,
        'paid': order.paid,
        'transactions': order.transactions,
        'order_url': request.build_absolute_uri('/orders/order/'
                                                + str(order.id)),
    }
    # order_html = render_to_string(
    #     "payment/order_details.html", context=context)
    order_html = render_to_string(
        'mail/order-confirmation.html', context=context)
    order_text = strip_tags(order_html)
    # print(order_text)
    EmailThread(
        subject=subject,
        text_content=order_text,
        from_email=from_email,
        html_content=order_html,
        recipient=recipient,
    ).start()


def send_otp(user, otp, create_ac=False):
    # print("mail send attempt")
    from_email = settings.EMAIL_HOST_USER
    recipient = [user.email]
    subject = "Password change requested"
    order_html = render_to_string('mail/otp.html',
                                  context={
                                      'otp': otp,
                                      'create_ac': create_ac
                                  })
    order_text = strip_tags(order_html)
    # print(order_text)
    EmailThread(
        subject=subject,
        text_content=order_text,
        from_email=from_email,
        html_content=order_html,
        recipient=recipient,
    ).start()
    # print("mail send done")


def payment_recieved(transaction):
    # print("mail send attempt")
    order = transaction.order
    from_email = settings.EMAIL_HOST_USER
    recipient = [order.user.email]
    subject = "Payment for Order #{id} received".format(id=order.id)
    context = {
        'order': order,
        'paid': order.paid,
        'transaction': transaction,
    }
    order_html = render_to_string(
        'mail/payment-confirmation.html', context=context)
    order_text = strip_tags(order_html)
    # print(order_text)
    EmailThread(
        subject=subject,
        text_content=order_text,
        from_email=from_email,
        html_content=order_html,
        recipient=recipient,
    ).start()
    # print("mail send done")


def subscribed(mail):
    from_email = settings.EMAIL_HOST_USER
    recipient = [mail, ]
    subject = "Subscribed to Panaya news letter"
    order_html = render_to_string('mail/subscribe.html',)
    order_text = strip_tags(order_html)
    # print(order_text)
    EmailThread(
        subject=subject,
        text_content=order_text,
        from_email=from_email,
        html_content=order_html,
        recipient=recipient,
    ).start()


def test(request):
    order = Order.objects.get(id=62)
    # order_confirmation(request,order)
    return render(request,
                  'mail/order-confirmation.html',
                  context={'order': order}
                  )
