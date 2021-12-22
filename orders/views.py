from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from user_manager.models import UserAddress
from cart.cart import Cart
from .forms import OrderCreateForm


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
    if request.method == 'POST':
        addr_id = request.POST['addrId'] if (
            'addrId' in request.POST) else request.user.addresses.all()[0]
        order = Order.objects.create(
            address_id=request.POST['addrId']
        )
        for item in cart:
            OrderItem.objects.create(order=order,
                                     product=item['product'],
                                     price=item['price'],
                                     quantity=item['quantity'])

        cart.clear()
        # return HttpResponse('order created')
        return render(request,
                      'orders/order/created.html',
                      context={'order': order})
    else:
        return HttpResponseBadRequest
