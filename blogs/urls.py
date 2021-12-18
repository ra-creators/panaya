from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogandnews, name="blogs"),
    path('<int:blogId>', views.blog, name="blog"),
    path('<int:blogId>/like', views.blog_like, name="blog_like"),
    # API to post a comment
    path('comments/<int:blogId>', views.comments, name="comments"),
]
