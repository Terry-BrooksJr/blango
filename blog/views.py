from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpRequest, HttpResponse

from blog.models import Post 
# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    context = {}
    posts = Post.objects.all()
    context['posts'] = posts
    return render(request, 'blog/index.html', context)


def post_detail(request: HttpRequest, slug: str) -> HttpResponse:
    context = {}
    post = get_object_or_404(Post, slug=slug)
    context['post'] = post
    return render(request, "blog/post-detail.html", context)