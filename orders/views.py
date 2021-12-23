import json
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from user_manager.models import UserAddress
from cart.cart import Cart
from .forms import OrderCreateForm
import math
from razor_pay.models import RazorPayOrder

# razor pay
from razor_pay.razorpay_key import razorpay, razorpay_key


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
def verify_order(request):
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
                  'payment/order_verify_details.html',
                  context={'user': request.user, 'cart': cart, 'form': form,
                           'address': address})


@login_required
def order_details(request, order_id):
    context = {}
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order_data = {}
        order_data['key'] = razorpay_key['id']
        order_data['amount'] = math.floor(float(order.total)*100)
        order_data['currency'] = 'INR'
        order_data['name'] = order.name
        order_data['description'] = "Transaction"
        order_data['order_id'] = order.razorpay_order_id
        # context['order'] = order
        # print(order)
        context['status'] = 200
        context['rapay_data'] = order_data
        # print(order_data)
        return JsonResponse(context)
    context = {'order': order, 'paid': order.paid,
               'transactions': order.transactions}
    return render(request, 'payment/order_details.html', context=context)


@login_required
def create_order(request):
    cart = Cart(request)
    addr_id = ""
    context = {}
    if request.method == 'POST':
        try:
            addr_id = json.loads(request.body)['addrId']
        except:
            return JsonResponse({'status': 400, 'payload': 'malformed data'})
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

    try:
        order_data = {}
        order_data['amount'] = math.floor(float(order.total)*100)
        order_data['currency'] = 'INR'

        payment = razorpay.order.create(data=order_data)

        order.razorpay_order_id = payment['id']
        order.save()

        RazorPayOrder.objects.create(
            order=order,
            rp_id=payment['id']
        )
        context['status'] = 200
        context['redirect'] = '/orders/order/'+str(order.id)
        cart.clear()
    except:
        order.delete()
        context['status'] = 500
        context['payload'] = "razorpay api error"

    return JsonResponse(context)

    # return render(request,
    #               'payment/order_checkout.html',
    #               context=context)
    # return HttpResponse(json.dumps(context), content_type="application/json")
