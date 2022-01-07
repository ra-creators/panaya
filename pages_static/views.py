from django.shortcuts import render
from allauth.socialaccount.models import SocialAccount
# models
from blogs.models import Blog
from product.models import Product, Type, Category, Collection


def index_view(request):
    blogs = Blog.objects.all()
    types = Type.objects.all()
    categories = Category.objects.all()
    collection = Collection.objects.all()

    new_products = Product.objects.order_by('-id')[:10]
    new_products = reversed(new_products)

    context = {
        'blogs': blogs,
        'types': types,
        'categories': categories,
        'collection': collection,
        'new_products': new_products,
    }

    if request.user.is_authenticated and request.user.fname == "":
        y = SocialAccount.objects.filter(user=request.user)[0]
        name = y.extra_data['name']
        request.user.fname = name.split(' ')[0]
        request.user.lname = " ".join(name.split(' ')[1:])
        request.user.save()

    return render(request, 'pages_static/index.html', context=context)


def about_view(request):
    return render(request, 'pages_static/about.html')


def contact_view(request):
    return render(request, 'pages_static/contactUs.html')


def tnc(request):
    return render(request, 'pages_static/policies/tnc.html')


def privacy_policy(request):
    return render(request, 'pages_static/policies/privacy_policy.html')


def delivery_shipping(request):
    return render(request, 'pages_static/policies/delivery_shipping.html')


def returns(request):
    return render(request, 'pages_static/policies/returns.html')
