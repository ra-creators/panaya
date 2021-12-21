from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import OrderItem
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
    return render(request, 'payment/order_address.html', context=context)


@login_required
def add_address(request):
    context = {}
    user = request.user
    context['user'] = user
    return render(request, 'payment/order_add_address.html', context=context)


# def order(request):
#     context = {}
#     user = request.user
#     context['user'] = user
#     return render(request, 'payment/order_order_details.html',
# context=context)

@login_required
def order(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])

            cart.clear()
            return render(request,
                          'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request,
                  'payment/order_order_details.html',
                  {'cart': cart, 'form': form})
