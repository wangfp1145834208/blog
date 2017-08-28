from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import markdown

from comments.forms import CommentForm
from .models import Post, Category

def index(request):
    post_list = Post.objects.all()
    context = {'post_list': post_list,
            'title': 'Black & White',
            }
    return render(request, 'blogs/index.html', context=context)

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body,
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
                ])
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {
            'post': post,
            'form': form,
            'comment_list': comment_list,
            'title': post.title,
            }
    return render(request, 'blogs/detail.html', context=context)

def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    )
    context = {
            'post_list': post_list,
            'title': 'archives',
            }
    return render(request, 'blogs/index.html', context=context)

def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    context = {
            'post_list': post_list,
            'title': 'category_'+cate.name,
            }
    return render(request, 'blogs/index.html', context=context)
