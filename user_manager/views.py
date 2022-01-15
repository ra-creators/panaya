import json
from django.http.response import HttpResponseBadRequest, HttpResponseNotFound
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.contrib import messages

# models
from .models import OTP
from orders.models import Order
# helper
from .helpers import generate_otp
from orders.helpers import trackOrder
# mail util
from util_mail.views import send_otp


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
            try:
                fname = request.POST.get("first_name")
                lname = request.POST.get("last_name")
                dob = request.POST.get("date_of_birth")
                phone = request.POST.get("phone")
                profile_pic = request.FILES.get('profile_pic')
                if profile_pic:
                    user = User.objects.create_user(email=email,
                                                    fname=fname,
                                                    lname=lname,
                                                    dob=dob,
                                                    phone_number=phone,
                                                    password=password,
                                                    profile_pic=profile_pic)
                else:
                    user = User.objects.create_user(email=email,
                                                    fname=fname,
                                                    lname=lname,
                                                    dob=dob,
                                                    phone_number=phone,
                                                    password=password)
                user.save()
                return redirect('index')
            except Exception as e:
                print(e)
                messages.error(request, 'Invalid signup')
                return redirect('signup')
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
        user = User.objects.get(email=email)
        # Check if OTP key already exists and override it if exists
        if not OTP.objects.filter(email=email).exists():
            otp = OTP.objects.create(
                email=email,
                otp=otp_
            )
        else:
            otp = OTP.objects.get(email=email)
            otp.otp = otp_
            otp.save()
        # Send OTP to user's email
        send_otp(user, otp_)
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
            otp_ = OTP.objects.get(email=email)
            # print(otp_.verify(otp))
            otp_res = otp_.verify(otp)
            # print(otp_res)
            if otp_res['status']:
                request.session['password_change'] = True
                return redirect('password_change')
            elif otp_res['case'] == 1:
                messages.error(request, 'Invalid OTP')
                return redirect('otp_check')
            else:
                messages.error(request, otp_res['payload'])
                return redirect('forgot_password')

            # if otp == otp_.otp:
            #     if otp_.created + timedelta(minutes=15) > timezone.make_aware(datetime.now()):
            #         messages.error(request, 'OTP Expired')
            #         return redirect('forgot_password')
            #     request.session['password_change'] = True
            #     return redirect('password_change')
            # else:
            #     messages.error(request, 'Invalid OTP')
            #     return redirect('otp_check')
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


class ProfileAddAddress(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user_manager/profile_add_address.html')

    def post(self, request):
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        address = request.POST.get('address').title()
        city = request.POST.get('city').title()
        postal_code = request.POST.get('postalcode')
        state = request.POST.get('state').title()
        country = request.POST.get('country').title()
        if len(postal_code) != 6:
            messages.error(request, "Postal Code Length should be 6")
            return redirect('add_address')
        if fname and lname and address and city and postal_code:
            address_ = request.user.addresses.create(
                user=request.user,
                first_name=fname,
                last_name=lname,
                address=address,
                city=city,
                postal_code=postal_code,
                state=state,
                country=country,
            )
            address_.save()
            messages.success(request, "Address added successfully")
            # if request.session.get('create'):
            #     del request.session['create']
            #     return redirect('create_order')
            # elif request.session.get('product_id'):
            #     product_id = request.session.get('product_id')
            #     del request.session['product_id']
            #     return redirect('buy_now', product_id)
            redirect_to = request.session.get('rd_to')
            # print(redirect_to)
            if redirect_to == 'address':
                del request.session['rd_to']
                return redirect('address')
            elif redirect_to == 'buy_now':
                product_id = request.session.get('product_id')
                del request.session['rd_to']
                del request.session['product_id']
                return redirect('buy_now', product_id)
            return redirect('create_order')
        else:
            messages.error(request, "Invalid")
            return redirect('add_address')


@login_required
def profile_delete_address(request):
    if request.method == 'POST':
        address_id = request.POST.get('id')
        if address_id:
            address = request.user.addresses.get(id=address_id)
            if address:
                address.delete()
                return redirect('address')
        else:
            return HttpResponseNotFound()
    return HttpResponseBadRequest()


@login_required
def profile_edit_address(request):
    if request.method == 'POST':
        address_id = request.POST.get('id')
        if address_id:
            address = request.user.addresses.get(id=address_id)
            if address:
                return render(request, 'user_manager/profile_edit_address.html', {"address": address})
        else:
            return HttpResponseNotFound()
    return HttpResponseBadRequest()


@login_required
def profile_edit_address_success(request):
    if request.method == 'POST':
        # print("hello")
        address_id = request.POST.get('id')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        postal_code = request.POST.get('postalcode')
        if address_id:
            # print("hi")
            address_ = request.user.addresses.get(id=address_id)
            if address_:
                address_.first_name = fname
                address_.last_name = lname
                address_.address = address
                address_.city = city
                address_.country = country
                address_.state = state
                address_.postal_code = postal_code
                address_.save()
                return redirect('address')
        else:
            return HttpResponseNotFound()
    return HttpResponseBadRequest()


@login_required
def orders_tracking(request):
    return render(request, 'user_manager/orders.html')


@login_required
def profile(request):
    return render(request, 'user_manager/profile.html')


@login_required
def profile_address(request):
    # for k, v in request.session.items():
    #     print(k, v)
    if request.session.get('rd_to'):
        del request.session['rd_to']
    # print(request.session.get('rd_to'))
    request.session['rd_to'] = 'address'
    # print(request.session.get('rd_to'))
    return render(request, 'user_manager/profile_address.html')


@login_required
@csrf_exempt
def update_phone(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        phone_number = json.loads(request.body)['phone_number']
        user.phone_number = str(phone_number)
        user.save()
        return HttpResponse(200)
    return HttpResponse(400)


@login_required
def single_order_detail(request, order_id):
    order = Order.objects.filter(id=order_id)[0]
    if request.user != order.user:
        return HttpResponseBadRequest
    return render(request, 'user_manager/order_details.html', {
        'order': order
    })

@login_required
def get_order_tracking(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.user != order.user:
        return HttpResponseBadRequest
    res = trackOrder(order)
    if res:
        return JsonResponse(res, safe=False)
    else:
        return JsonResponse({'status_code':404, 'text':"Not Found"})