# python imports
import math
import json

# django imports
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, JsonResponse

# models
from product.models import Product
from .models import Order, OrderItem
# from user_manager.models import UserAddress
from razor_pay.models import RazorPayOrder

# forms
# from .forms import OrderCreateForm

# razor pay
from razor_pay.razorpay_key import razorpay, razorpay_key

# utils
from cart.cart import Cart
from .helpers import createNewOrder
from util_mail.views import order_confirmation


@login_required
def verify_order(request, product_id=None):
    context = {}

    cart = Cart(request)
    context['cart'] = cart

    user = request.user
    context['user'] = user

    if(product_id):
        product = Product.objects.get(id=product_id)
        cart = {
            'product': product,
            'quantity': 1,
            'total_price': product.price,
        }
        context['cart'] = [cart]

    context['addresses'] = user.addresses.all()

    return render(request,
                  'payment/order_verify_details.html',
                  context=context)


@login_required
def buy_now(request, product_id):
    context = {}
    quantity = 1
    request.session['rd_to'] = 'buy_now'
    request.session['product_id'] = product_id
    if(request.method == 'POST' and 'quantity' in request.POST):
        quantity = int(request.POST['quantity'])

    user = request.user
    context['user'] = user

    product = Product.objects.get(id=product_id)
    cart = {
        'product': product,
        'quantity': quantity,
        'total_price': product.price,
    }
    context['cart'] = [cart]

    context['addresses'] = user.addresses.all()
    return render(request,
                  'payment/order_verify_details.html',
                  context=context)


def undo_create_order(order, status, msg, err):
    print(err)
    try:
        order.delete()
    except Exception as exc_err:
        print(exc_err)
        pass
    context = {}
    context['msg'] = msg
    context['error'] = err
    context['status'] = status
    return JsonResponse(context)


def create_invoice(order):
    user = order.user
    address = order.address
    address = {
        'line1': address.line1,
        'line2': address.line2,
        'city': address.city,
        'zipcode': address.postal_code,
        'state': address.state,
        'country': address.country,
    }
    customer = {
        'name': user.get_full_name(),
        'email': user.email,
        'contact': user.phone_number,
        'billing_address': address,
        'shipping_address': address,
    }
    line_items = []
    for item in order.items.all():
        line_items.append(
            {
                'name': item.product.name,
                'amount': int(item.product.price*100),
                'quantity': item.quantity,
            }
        )
    data = {
        'type': 'invoice',
        'description': 'Invoice for Order',
        # 'description': ('Invoice for Order #{order_id}'
        #                 .format(order_id=order.id)),
        'customer': customer,
        'line_items': line_items,
        'currency': 'INR',
    }
    invoice = razorpay.invoice.create(data=data)
    return invoice


@login_required
def create_order(request):
    if request.method == 'GET':
         # request.session['rd_to'] = 'create_order'
        return verify_order(request)
    cart = Cart(request)
    addr_id = ""
    context = {}

    if request.method != 'POST':
        return HttpResponse("no allowed")
    # quick fix for address redirect issue

    post_data = json.loads(request.body)
    if('addrId' not in post_data or 'items' not in post_data):
        return JsonResponse({'status': 400, 'payload': 'malformed data'})

    addr_id = json.loads(request.body)['addrId']
    items = json.loads(request.body)['items']
    requesting_url = json.loads(request.body)['requestingUrl']

    if cart.coupon:
        order = Order.objects.create(
            user=request.user,
            address_id=addr_id,
            coupon=cart.coupon,
        )
    else:
        order = Order.objects.create(
            user=request.user,
            address_id=addr_id,
        )

    try:
        for item in items:
            # print(item)
            item['quantity'] = int(item['quantity'])
            OrderItem.objects.create(
                order=order,
                product_id=item['id'],
                price=Product.objects.get(id=item['id']).price,
                quantity=item['quantity'])
    except Exception as e:
        # print(e)
        # order.delete()
        return undo_create_order(order, 400, 'malformed data', str(e))
    # print(order)

    # print('pre razorcall', order.coupon, order.discount, order.total)
    # order.save()

    # try:
    #     order_tracking = createNewOrder(order)
    #     if not order_tracking:
    #         raise Exception('Order is not created')
    # except Exception as e:
    #     print(e)

    try:
        order_data = {}
        # print('razorcall', order.coupon, order.discount, order.total)
        # print(order.total, order.total*100)
        order_data['amount'] = ((order.total)*100)
        order_data['currency'] = 'INR'

        payment = razorpay.order.create(data=order_data)
        # invoice = create_invoice(order)
        order.razorpay_order_id = payment['id']
        # order.razorpay_invoice_id = invoice['id']
        # order.save()

        RazorPayOrder.objects.create(
            order=order,
            rp_id=payment['id']
        )
        context['status'] = 200
        context['redirect'] = '/orders/order/'+str(order.id)
        if(requesting_url == '/orders/create/'):
            cart.clear()
    except Exception as e:
        # print('razorpay exception :', e)
        # order.delete()
        return undo_create_order(order, 500, "razorpay api error", str(e))
    try:
        order_confirmation(request, order)
    except Exception as err:
        print("email error", err)
    
    order.save()
    try:
        order_tracking = createNewOrder(order)
        print("ORDER TRACKING: ", order_tracking)
        if not order_tracking:
            raise Exception('Order is not created')
    except Exception as e:
        print(e)

    
    return JsonResponse(context)

    # return render(request,
    #               'payment/order_checkout.html',
    #               context=context)
    # return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
def order_details(request, order_id):
    context = {}
    order = get_object_or_404(Order, id=order_id)
    # print('details', order.coupon, order.discount, order.total)
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
