from django.urls import path
from . import views

urlpatterns = [
    path('api/add_contact_email/', views.contactUsEmailSend, name='contactUsEmailSend'),
    path('api/add_contact/', views.connectUs, name='contact_us'),
]
