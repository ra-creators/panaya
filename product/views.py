from django.shortcuts import render, get_object_or_404, HttpResponse
from django.core.paginator import Paginator
from .models import Category, Product
from cart.forms import CartAddProductForm
# Create your views here.


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'product/list.html',
                  {
                      'category': category,
                      'categories': categories,
                      'products': products
                  })


def product_detail(request, id, slug=None):
    if slug:
        product = get_object_or_404(Product,
                                    id=id,
                                    slug=slug,
                                    available=True)
    else:
        product = get_object_or_404(Product,
                                    id=id,
                                    available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})


# @require_POST
def product_search(request):
    context = {}
    context['formdata'] = {}
    searched_products = Product.objects
    if request.method == 'POST':
        # print(request.POST)
        post_data = request.POST

        context['formdata']['name'] = post_data['name']
        if(post_data['name'] != ''):
            # print('name')
            searched_products = searched_products.filter(
                name__icontains=post_data['name'])

        context['formdata']['category'] = post_data['category']
        if(post_data['category'] != ''):
            # print('cat')
            searched_products = searched_products.filter(
                category=post_data['category'])

        context['formdata']['maxPrice'] = post_data['maxPrice']
        if(post_data['maxPrice'] != ''):
            # print('maxpr')
            searched_products = searched_products.filter(
                price__gte=post_data['maxPrice'])

        context['formdata']['minPrice'] = post_data['minPrice']
        if(post_data['minPrice'] != ''):
            # print('minpr')
            searched_products = searched_products.filter(
                price__lte=post_data['minPrice'])
        # pages = Paginator(searched_products, 24)
        # context['pages'] = pages
        # print(pages)
    else:
        context['formdata']['name'] = ''
        context['formdata']['category'] = ''
        context['formdata']['maxPrice'] = ''
        context['formdata']['minPrice'] = ''
        searched_products = searched_products.all()
    # print(searched_products)
    context['products'] = searched_products
    context['categories'] = Category.objects.all()
    return render(request, 'product/list.html', context=context)


def cart(request):
    return render(request, 'product/cart.html')
