from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Category, Product, Collection, Type
from cart.forms import CartAddProductForm
# Create your views here.


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    # print(category_slug)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'product/list.html',
                  {
                      'category': category,
                      'categories': categories,
                      'products': products.all()
                  })


def categories(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    # print(category_slug)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        categories = [category]
        products = products.filter(category=category)
    return render(request,
                  'product/categories.html',
                  {
                      'category': category,
                      'categories': categories,
                      'products': products
                  })


def collections(request, collection_slug=None):
    collection = None
    collections = Collection.objects.all()
    products = Product.objects.filter(available=True)
    print(collection_slug)
    if collection_slug:
        collection = get_object_or_404(Collection, slug=collection_slug)
        collections = [collection]
        products = products.filter(collection=collection)
    return render(request,
                  'product/collections.html',
                  {
                      'collections': collections,
                      'products': products
                  })


def types(request, type_slug=None):
    type = None
    types = Type.objects.all()
    products = Product.objects.filter(available=True)
    print(type_slug)
    if type_slug:
        type = get_object_or_404(Type, slug=type_slug)
        types = [type]
        products = products.filter(type=type)
    return render(request,
                  'product/types.html',
                  {
                      'types': types,
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
    related = product.realted()
    faqs = product.faqs
    # print(related)
    return render(request,
                  'product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   'related': related,
                   'faqs': faqs,
                   })


# @require_POST
def product_search(request, page=1):
    context = {}
    context['formdata'] = {}
    context['number_pages'] = 1
    searched_products = Product.objects
    if request.method == 'POST':
        # print(request.POST)
        post_data = request.POST

        try:
            context['formdata']['name'] = post_data['name']
            if(post_data['name'] != ''):
                # print('name')
                searched_products = searched_products.filter(
                    name__icontains=post_data['name'])
        except Exception as err:
            context['err'] = err
            pass

        try:
            context['formdata']['category'] = post_data['category']
            if(post_data['category'] != '0'):
                # print('cat')
                searched_products = searched_products.filter(
                    category=post_data['category'])
        except Exception as err:
            context['err'] = err
            pass

        try:
            context['formdata']['collection'] = post_data['collection']
            if(post_data['collection'] != '0'):
                # print('cat')
                searched_products = searched_products.filter(
                    collection=post_data['collection'])
        except Exception as err:
            context['err'] = err
            pass

        try:
            context['formdata']['type'] = post_data['type']
            if(post_data['type'] != '0'):
                # print('cat')
                searched_products = searched_products.filter(
                    type=post_data['type'])
        except Exception as err:
            context['err'] = err
            pass

        try:
            context['formdata']['maxPrice'] = post_data['maxPrice']
            if(post_data['maxPrice'] != ''):
                # print('maxpr')
                searched_products = searched_products.filter(
                    price__gte=post_data['maxPrice'])
        except Exception as err:
            context['err'] = err
            pass

        try:
            context['formdata']['minPrice'] = post_data['minPrice']
            if(post_data['minPrice'] != ''):
                # print('minpr')
                searched_products = searched_products.filter(
                    price__lte=post_data['minPrice'])
        except Exception as err:
            context['err'] = err
            pass
        searched_products = searched_products.all()
    else:
        context['formdata']['name'] = ''
        context['formdata']['category'] = ''
        context['formdata']['maxPrice'] = ''
        context['formdata']['minPrice'] = ''
        searched_products = searched_products.all()
    # print(searched_products)

    pages = Paginator(searched_products, 24)
    # print(pages)
    context['pages'] = pages
    context['number_pages'] = pages.num_pages
    # context['current_page'] = pages.page(page)
    context['current_page_number'] = (page)
    context['products'] = pages.page(1)
    context['categories'] = Category.objects.all()
    return render(request, 'product/list.html', context=context)


def cart(request):
    return render(request, 'product/cart.html')
