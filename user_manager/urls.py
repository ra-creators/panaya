from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('profile/home', views.profile, name='profile'),
    path('profile/address/', views.profile_address, name='address'),
    path('profile/add_address', views.ProfileAddAddress.as_view(), name='add_address'),
    path('profile/delete_address', views.profile_delete_address, name='delete_address'),
    path('proflie/edit_address', views.profile_edit_address, name='edit_address'),
    path('profile/profile_edit_address_success', views.profile_edit_address_success, name='profile_edit_address_success'),
    path('profile/orders_tracking', views.orders_tracking, name='orders_tracking'),
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('forgot_password/', views.ForgotPassword.as_view(), name='forgot_password'),
    path('otp_check/', views.OTPCheck.as_view(), name='otp_check'),
    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('profile/api/user/<int:user_id>/', views.update_phone, name='update_phone'),
]
