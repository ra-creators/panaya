from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Category, Product, Collection, Type, Review, Color
from pages_static.models import ShopSlider
from cart.forms import CartAddProductForm
# Create your views here.
# from django.contrib import messages


class product(View):
    def __init__(self):
        self.categories = Category.objects.all()
        self.types = Type.objects.all()
        self.colors = Color.objects.all()
        self.products = Product.objects.filter(available=True).all()
        self.shop_slider = ShopSlider.objects.all()[:5]
        self.context = {
            'categories': self.categories,
            'types': self.types,
            'colors': self.colors,
            'products': self.products,
            'ShopSlider': self.shop_slider,
        }

    def list(self, request, page=1):

        context = {
            'page': 'list',
        }
        pages = Paginator(self.products, 24)
        context['current_page_number'] = page
        context['products'] = pages.page(page)
        context['number_pages'] = pages.num_pages

        return render(request,
                      'product/list.html',
                      context=context
                      )

    def category(self, request, category_slug=None):
        category = None
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            categories = [category]
            products = self.products.filter(category=category)
        return render(request,
                      'product/categories.html',
                      {
                          'category': category,
                          'categories': categories,
                          'products': products
                      })

    def collection(self, request, collection_slug=None):
        collection = None
        if collection_slug:
            collection = get_object_or_404(Collection, slug=collection_slug)
            collections = [collection]
            products = self.products.filter(collection=collection)
        return render(request,
                      'product/categories.html',
                      {
                          'collection': collection,
                          'collections': collections,
                          'products': products
                      })

    def type(self, request, type_slug=None):
        type = None
        if type_slug:
            type = get_object_or_404(Type, slug=type_slug)
            types = [type]
            products = self.products.filter(type=type)
        return render(request,
                      'product/categories.html',
                      {
                          'type': type,
                          'types': types,
                          'products': products
                      })

    def product_search(request, page=1):
        context = {}
        context['formdata'] = {}
        context['number_pages'] = 1
        searched_products = Product.objects.filter(available=True)
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
                context['formdata']['type'] = post_data['type']
                if(post_data['type'] != '0'):
                    # print('cat')
                    searched_products = searched_products.filter(
                        type=post_data['type'])
            except Exception as err:
                context['err'] = err
                pass

            try:
                context['formdata']['color'] = post_data['color']
                if(post_data['color'] != '0'):
                    searched_products = searched_products.filter(
                        colors__id=post_data['color'])
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
            context['formdata']['type'] = ''
            context['formdata']['color'] = ''
            context['formdata']['product'] = ''
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
        context['types'] = Type.objects.all()
        context['colors'] = Color.objects.all()
        context['ShopSlider'] = ShopSlider.objects.all()[:5]
        return render(request, 'product/list.html', context=context)


def product_list(request, page=1):
    categories = Category.objects.all()
    types = Type.objects.all()
    colors = Color.objects.all()
    products = Product.objects.filter(available=True)

    context = {
        'page': 'list',
        'categories': categories,
        'types': types,
        'colors': colors,
        'products': products.all(),
        'ShopSlider': ShopSlider.objects.all()[:5]
    }
    pages = Paginator(products, 24)
    context['current_page_number'] = page
    context['products'] = pages.page(page)
    context['number_pages'] = pages.num_pages

    return render(request,
                  'product/list.html',
                  context=context
                  )


def categories(request, category_slug=None, page=1):
    context = {}
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    context['page_heading'] = 'Categories'
    context['page_type'] = 'list'
    context['single_url'] = 'product_list_by_category'
    # print(category_slug)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        context['page_heading'] = ('Categories | '+category.name)
        context['page_type'] = 'single'
        categories = [category]
        products = products.filter(category=category)
        pages = Paginator(products, 24)
        context['current_page_number'] = page
        products = pages.page(page)
        context['number_pages'] = pages.num_pages
    context.update({
        'property': category,
        'properties': categories,
        'products': products,
        'ShopSlider': ShopSlider.objects.all()[:5],
    })
    return render(request,
                  'product/properties.html',
                  context=context
                  )


def collections(request, collection_slug=None, page=1):
    context = {}
    collection = None
    collections = Collection.objects.all()
    products = Product.objects.filter(available=True)
    context['page_heading'] = 'Collections'
    context['page_type'] = 'list'
    context['single_url'] = 'product_list_by_collection'
    # print(collection_slug)
    if collection_slug:
        collection = get_object_or_404(Collection, slug=collection_slug)
        collections = [collection]
        context['page_heading'] = ('Collections | '+collection.name)
        context['page_type'] = 'single'
        products = products.filter(collection=collection)
        pages = Paginator(products, 24)
        context['current_page_number'] = page
        products = pages.page(page)
        context['number_pages'] = pages.num_pages
    context.update({
        'property': collection,
        'properties': collections,
        'products': products,
        'ShopSlider': ShopSlider.objects.all()[:5],
    })
    return render(request,
                  'product/properties.html',
                  context=context
                  )


def types(request, type_slug=None, page=1):
    context = {}
    type = None
    types = Type.objects.all()
    products = Product.objects.filter(available=True)
    context['page_heading'] = 'Types'
    context['page_type'] = 'list'
    context['single_url'] = 'product_list_by_type'
    # print(type_slug)
    if type_slug:
        type = get_object_or_404(Type, slug=type_slug)
        types = [type]
        context['page_heading'] = ('Types | '+type.name)
        context['page_type'] = 'single'
        products = products.filter(type=type)
        pages = Paginator(products, 24)
        context['current_page_number'] = page
        products = pages.page(page)
        # print(products)
        context['number_pages'] = pages.num_pages
    # print(products)
    context.update({
        'property': type,
        'properties': types,
        'products': products,
        'ShopSlider': ShopSlider.objects.all()[:5],
    })
    return render(request,
                  'product/properties.html',
                  context=context
                  )


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
    lst = []
    # Check if related product is available or not
    for i in related:
        if i.available:
            lst.append(i)
    related = set(lst)

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
    searched_products = Product.objects.filter(available=True)
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
            context['formdata']['type'] = post_data['type']
            if(post_data['type'] != '0'):
                # print('cat')
                searched_products = searched_products.filter(
                    type=post_data['type'])
        except Exception as err:
            context['err'] = err
            pass

        try:
            context['formdata']['color'] = post_data['color']
            if(post_data['color'] != '0'):
                searched_products = searched_products.filter(
                    colors__id=post_data['color'])
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
        context['formdata']['type'] = ''
        context['formdata']['color'] = ''
        context['formdata']['product'] = ''
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
    context['products'] = pages.page(page)
    context['categories'] = Category.objects.all()
    context['types'] = Type.objects.all()
    context['colors'] = Color.objects.all()
    context['ShopSlider'] = ShopSlider.objects.all()[:5]
    return render(request, 'product/list.html', context=context)


def cart(request):
    if request.session.get('rd_to'):
        del request.session['rd_to']
    # print(request.session.get('rd_to'))
    return render(request, 'product/cart.html')


@csrf_exempt
@login_required
def feedback_product(request):
    if request.method == 'POST':
        rating = request.POST.get('feedback')
        text = request.POST.get('text')
        product_id = request.POST.get('product_id')
        order_id = request.POST.get('order_id')
        print(rating, text, product_id, order_id)
        p = Product.objects.get(id=product_id)
        p.update_rating(int(rating))
        p.save()
        Review.objects.create(
            product=p,
            user=request.user,
            stars=int(rating),
            body=text
        )
        return redirect('single_order', order_id)
    return redirect('index')
