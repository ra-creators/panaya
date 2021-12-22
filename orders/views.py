import json
from django.http.response import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from user_manager.models import UserAddress
from cart.cart import Cart
from .forms import OrderCreateForm
import math
from django.views.decorators.csrf import csrf_exempt


# razor pay
import razorpay
razorpay_key = {'id': "rzp_test_zQH7ZMXqeZqmAK",
                'secret': 'BQZqkIzVpS70aYSEcF0t5Pnb'}
razorpay = razorpay.Client(
    auth=("rzp_test_zQH7ZMXqeZqmAK", "BQZqkIzVpS70aYSEcF0t5Pnb"))


@login_required
def start(request):
    context = {}
    user = request.user
    context['user'] = user
    return render(request, 'payment/order_start.html', context=context)


@login_required
def address(request):
    context = {}
    user = request.user
    context['user'] = user
    context['addresses'] = user.addresses.all()
    return render(request, 'payment/order_address.html', context=context)


@login_required
def add_address(request):
    context = {}
    user = request.user
    context['user'] = user
    return render(request, 'payment/order_add_address.html', context=context)


@login_required
def order(request):
    cart = Cart(request)
    address = ''
    if(request.method == 'POST'):
        addr_id = request.POST['addrId']
        address = get_object_or_404(UserAddress, id=addr_id)
    else:
        address = request.user.addresses.all()[0]
    # request.session['address'] = str(address.id)
    # print(address.id)
    form = OrderCreateForm()
    return render(request,
                  'payment/order_order_details.html',
                  context={'cart': cart, 'form': form, 'address': address})


@login_required
def create_order(request):
    cart = Cart(request)
    addr_id = ""
    context = {}
    if request.method == 'POST':
        try:
            addr_id = json.loads(request.body)['addrId']
        except:
            return JsonResponse({'status': 400})
    else:
        addr_id = request.user.addresses.all()[0].id
    order = Order.objects.create(
        user=request.user,
        address_id=addr_id
    )
    for item in cart:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            price=item['price'],
            quantity=item['quantity'])

    # cart.clear()
    # return HttpResponse('order created')
    order_data = {}
    order_data['amount'] = math.floor(float(order.total)*100)
    order_data['currency'] = 'INR'
    payment = razorpay.order.create(data=order_data)
    order.razorpay_order_id = payment['id']
    order_data['name'] = order.name
    order_data['description'] = "Transaction"
    order_data['order_id'] = payment['id']

    # context['order'] = order
    # print(order)
    context['rapay_data'] = order_data

    context['status'] = 200
    # return render(request,
    #               'payment/order_checkout.html',
    #               context=context)
    return HttpResponse(json.dumps(context), content_type="application/json")
    # return JsonResponse(context)


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
    try:
        res = razorpay.utility.verify_payment_signature(data)
        return HttpResponse('payment success')
    except:
        return HttpResponse('payment failure')
