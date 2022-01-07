from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    # policies
    path('policies/terms&conditions', views.tnc, name='tnc'),
    path('policies/returns', views.returns, name='return_policy'),
    path('policies/privacy-policies',
         views.privacy_policy, name='privacy_policy'),
    path('policies/delivery&shipping',
         views.delivery_shipping, name='delivery_shipping'),

]
