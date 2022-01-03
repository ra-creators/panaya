from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string
# from mail import send_mail
from django.core.mail import send_mail as django_send_mail


def send_mail(user, otp,):
    # print("mail send attempt")
    from_email = settings.EMAIL_HOST_USER
    recipient = [user.email]
    subject = "Password change requested"
    order_html = "Hei,<br/> {user_name}, Here is the otp <h2>{otp}</h2> to reset password".format(user_name=user.get_full_name(), otp=str(otp))
    order_text = strip_tags(order_html)
    # print(order_text)
    django_send_mail(
        subject=subject,
        message=order_text,
        html_message=order_html,
        from_email=from_email,
        recipient_list=recipient,
    )
    # print("mail send done")