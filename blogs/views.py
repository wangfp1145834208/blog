from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Post

def index(request):
    post_list = Post.objects.all()
    context = {'post_list': post_list}
    return render(request, 'blogs/index.html', context=context)

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blogs/detail.html', context={'post': post})
