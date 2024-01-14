from django.shortcuts import render
from django.utils import timezone
from django.http import HttpRequest, HttpResponse

from blog.models import Post 
# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    context = {}
    posts = Post.objects.all()
    context['posts'] = posts
    return render(request, 'blog/index.html', context);