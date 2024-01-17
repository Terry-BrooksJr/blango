from django.urls import path
from blog import views

urlpatterns = [
    path("", views.index, name="blog-index"),
    path("post/<slug:slug>/", views.post_detail, name="post-detail"),
]
