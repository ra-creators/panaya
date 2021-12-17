from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()

class UserLogin(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponse('You are already logged in')
        return render(request, 'user_manager/login.html')

    def post(self, request):
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

def user_logout(request):
    logout(request)
    return redirect('login')

class SignUpView(View):
    """Using dummy signup class for now"""
    def get(self, request):
        return render(request, 'user_manager/signup.html')

    def post(self, request):
        email = request.POST.get("email")
        if User.objects.filter(email=email).exists():
            return HttpResponse('Email already exists')
        password = request.POST.get("password")
        password2 = request.POST.get('password2')
        if password != password2:
            return HttpResponse('Passwords do not match')
        if email and password:
            fname = request.POST.get("first_name")
            lname = request.POST.get("last_name")
            dob = request.POST.get("date_of_birth")
            user = User.objects.create_user(email=email,
                                            fname=fname,
                                            lname=lname,
                                            dob=dob,
                                            password=password)
            user.save()
            return HttpResponse('User created successfully')
        else:
            return HttpResponse('Invalid')