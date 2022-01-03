from django.template.loader import render_to_string
# from django.conf import settings
# from mail import send_mail
from django.core.mail import send_mail

def tst_mail():
    # print("mail send attempt")
    # from_email = settings.EMAIL_HOST_USER
    from_email = "noreply@panaya.in"
    recipient = ["ab.inpathtoadev@gmail.com"]
    subject = "Order #{id} placed".format(id=15)
    # context = {
    #     'order': order,
    #     'paid': order.paid,
    #     'transactions': order.transactions,
    #     'order_url': request.build_absolute_uri('/orders/order/'+str(order.id)),
    # }
    # order_html = render_to_string(
    #     "payment/order_details.html", context=context)
    # order_text = render_to_string(
        # 'payment/order_confirmation.html', context=context)
    # print(order_text)
    order_text = 'terst ststets'
    send_mail(subject=subject, message=order_text, from_email=from_email, html_message=order_text,
              recipient_list=recipient, )
    # print("mail send done")


if __name__ == '__main__':
    # pass
    tst_mail()
