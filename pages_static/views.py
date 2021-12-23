from django.shortcuts import render

# Create your views here.


def index_view(request):
    return render(request, 'pages_static/index.html')


def about_view(request):
    return render(request, 'pages_static/about.html')


def contact_view(request):
    return render(request, 'pages_static/contactUs.html')


def tnc(request):
    return render(request, 'pages_static/tnc.html')


def privacy_p1(request):
    return render(request, 'pages_static/privacy_p1.html')


def privacy_p2(request):
    return render(request, 'pages_static/privacy_p2.html')


