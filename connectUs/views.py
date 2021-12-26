from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import ConnectEmails, ConnectUs
# Create your views here.
@csrf_exempt
def contactUsEmailSend(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if ConnectEmails.objects.filter(email=email).exists():
            return HttpResponse(400)
        email_ = ConnectEmails.objects.create(email=email)
        email_.save()
        return HttpResponse(200)
    return HttpResponseBadRequest()

@csrf_exempt
def connectUs(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        name = request.POST.get('name')
        query = request.POST.get('query')
        if email and phone and name and query:
            obj = ConnectUs.objects.create(
                email=email, phone=phone, name=name, query=query)
            obj.save()
            return HttpResponse(200)
        return HttpResponse(400)
    return HttpResponseBadRequest()