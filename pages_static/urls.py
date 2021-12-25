from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    # policies
    path('policies/terms&conditions', views.tnc, name='tnc'),
    path('policies/privacy-policies-page-1',
         views.privacy_p1, name='privacy_p1'),
    path('policies/privacy-policies-page-2',
         views.privacy_p2, name='privacy_p2'),

]
