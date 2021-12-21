from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from product.models import Product
from .cart import Cart
from .forms import CartAddProductForm
import json

# Create your views here.


@require_POST
def cart_add(request, ):
    product_req = (json.loads(request.body))
    cart = Cart(request)
    if('id' not in product_req and 'quantity' not in product_req):
        return HttpResponse(400)

    product = get_object_or_404(Product, id=product_req['id'])
    cart.add(product=product,
             quantity=product_req['quantity'],
             override=True)
    return HttpResponse(200)
    # return redirect('cart_detail')


@require_POST
def cart_remove(request,):
    cart = Cart(request)
    product_req = json.loads(request.body)
    if('id' not in product_req):
        return HttpResponse(400)
    product = get_object_or_404(Product, id=product_req['id'])
    cart.remove(product)
    return HttpResponse(200)
    # return redirect('cart_detail')


def cart_detail(request):
    return redirect('cart')
    # cart = Cart(request)
    # for item in cart:
    #     item['update_quantity_form'] = CartAddProductForm(initial={
    #         'quantity': item['quantity'],
    #         'override': True})
    # print(cart)
    # return HttpResponse(200)
    # return render(request, 'cart/detail.html', {'cart': cart})
