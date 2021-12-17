from django.conf.urls import url
from django.urls import path
# from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    # path('password_change/',
    #      auth_views.PasswordChangeView.as_view(),
    #      name='password_change'),
    # path('password_change/done/',
    #      auth_views.PasswordChangeDoneView.as_view(),
    #      name='password_change_done')
]
