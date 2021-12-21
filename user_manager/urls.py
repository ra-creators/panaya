from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('forgot_password/', views.ForgotPassword.as_view(), name='forgot_password'),
    path('otp_check/', views.OTPCheck.as_view(), name='otp_check'),
    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
]
