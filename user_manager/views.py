from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import OTP
from .helpers import *
# Create your views here.

User = get_user_model()

class UserLogin(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
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
                return redirect('index')
            else:
                messages.error(request, 'Invalid Credentials')
                return redirect('login')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')

def user_logout(request):
    logout(request)
    return redirect('login')

class SignUpView(View):
    """Using dummy signup class for now"""
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, 'user_manager/signup.html')

    def post(self, request):
        email = request.POST.get("email")
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('signup')           
        password = request.POST.get("password")
        password2 = request.POST.get('password2')
        if password != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')
        if email and password:
            fname = request.POST.get("first_name")
            lname = request.POST.get("last_name")
            dob = request.POST.get("date_of_birth")
            phone = request.POST.get("phone")
            user = User.objects.create_user(email=email,
                                            fname=fname,
                                            lname=lname,
                                            dob=dob,
                                            phone_number=phone,
                                            password=password)
            user.save()
            return redirect('index')
        else:
            messages.error(request, 'Invalid signup')
            return redirect('signup')

class ForgotPassword(View):
    def get(self, request):
        return render(request, 'user_manager/forgot_password.html')

    def post(self, request):
        email = request.POST.get("email")
        if not User.objects.filter(email=email).exists():
            messages.error(request, 'Email doesn\'t exists')
            return redirect('forgot_password')
        otp_ = generate_otp()
        # Check if OTP key already exists and override it if exists
        if not OTP.objects.filter(user=User.objects.get(email=email)).exists():
            otp = OTP.objects.create(
                user=User.objects.get(email=email),
                otp=otp_
            )
        else:
            otp = OTP.objects.get(user=User.objects.get(email=email))
            otp.otp = otp_
            otp.save()
        # Send OTP to user's email

        request.session['email'] = email
        return redirect('otp_check')

class OTPCheck(View):
    def get(self, request):
        email = request.session.get('email')
        if email:
            return render(request, 'user_manager/otp_check.html', {"email": email})
        else:
            return redirect('forgot_password')

    def post(self, request):
        email = request.session.get("email")
        otp = request.POST.get('otp')
        if otp:
            otp_ = OTP.objects.get(user=User.objects.get(email=email))
            if otp == otp_.otp :
                request.session['password_change'] = True
                return redirect('password_change')
            else:
                messages.error(request, 'Invalid OTP')
                return redirect('otp_check')
        else:
            messages.error(request, 'Invalid OTP')
            return redirect('otp_check')

class PasswordChangeView(View):
    def get(self, request):
        if request.session.get('password_change') is None:
            return redirect('login')
        return render(request, 'user_manager/password_change_form.html')

    def post(self, request):
        if request.session.get('password_change') is None:
            return redirect('login')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password != password2:
            messages.error(request, "Passwords do not match")
            return redirect('password_change')
        email = request.session.get('email')
        user = User.objects.filter(email=email).first()
        user.set_password(password)
        user.save()
        del request.session['password_change']
        del request.session['email']
        messages.success(request, "Password changed successfully")
        return redirect('login')