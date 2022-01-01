from django.shortcuts import HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

# models
from .models import RazorPayOrder, Transaction
from orders.models import Order

# razor pay
from .razorpay_key import razorpay

# mail utils
from utils.mail import payment_recieved


@csrf_exempt
def rp_callback(request):
    if(request.method != 'POST'):
        return HttpResponse('400')

    data = request.POST
    # 'razorpay_payment_id': ['pay_IaT9NuYNMv0KPu'],
    # 'razorpay_order_id': ['order_IaT8u5a6oG3blH'],
    # 'razorpay_signature': ['e199055fa86a73800b9d0605d1578255838438b110c691c55fd643830d046c1d'],
    # 'org_logo': [''], # 'org_name': ['Razorpay Software Private Ltd'],
    # 'checkout_logo': ['https://cdn.razorpay.com/logo.png'], 'custom_branding': ['false']
    # print(data)
    try:
        res = razorpay.utility.verify_payment_signature(data)
    except:
        return HttpResponse('payment failure')

    try:
        order = Order.objects.get(razorpay_order_id=data['razorpay_order_id'])
        rp_order = RazorPayOrder.objects.get(order=order)
        transaction = Transaction.objects.create(
            order=order,
            razorpay_order=rp_order,
            payment_id=data['razorpay_payment_id'],
            payment_sig=data['razorpay_signature'],
        )
        order.paid = True
        order.save()
        try:
            payment_recieved.send_mail(
                request=request, transaction=transaction)
        except Exception as err:
            print(err)
        return redirect('order_details', order.id)
    except:
        return HttpResponse('error occured')
