from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def user_login(request):
    if request.user.is_authenticated:
        return HttpResponse('You are already logged in')
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        if email and password:
            user = authenticate(request,
                                email=email,
                                password=password)
            if user is not None:
                login(request, user)
                return HttpResponse('Authenticated successfully')
            else:
                return HttpResponse('Invalid login')
        else:
            return HttpResponse('Invalid')
    else:
        return render(request, 'user_manager/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')