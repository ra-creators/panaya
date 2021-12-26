from django.urls import path
from . import views

urlpatterns = [
    path('api/add_contact_email/', views.contactUsEmailSend, name='contactUsEmailSend'),
]
