from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpRequest, HttpResponse
from blog.forms import CommentForm 
from blog.models import Post, Comment
from django.contrib.contenttypes.models import ContentType


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    context = {}
    posts = Post.objects.all()
    context['posts'] = posts
    return render(request, 'blog/index.html', context)


def post_detail(request: HttpRequest, slug: str) -> HttpResponse:
    context = {} 
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all()
    if request.user.is_active:
        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.content_object = post
                new_comment.creator = request.user
                new_comment.save()
                return redirect(request.path_info)
        else:
            comment_form = CommentForm()
    else:
        comment_form = None
    context['post'] = post
    context['comments'] = comments
    context['form'] = comment_form
    print(context)
    return render(request, "blog/post-detail.html", context)