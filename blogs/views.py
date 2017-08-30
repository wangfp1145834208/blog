from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
import markdown

from comments.forms import CommentForm
from .models import Post, Category

class IndexView(ListView):
    model = Post
    template_name = 'blogs/index.html'
    context_object_name = 'post_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Black & White'
        context.update({'title': title})
        return context

class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs['pk'])
        return super().get_queryset().filter(category=cate)

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        cate = get_object_or_404(Category, pk=self.kwargs['pk'])
        title = cate.name + ' 类'
        context['title'] = title
        return context

class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        return super().get_queryset().filter(created_time__year=year,
                                            created_time__month=month)

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        year = self.kwargs['year']
        month = self.kwargs['month']
        title = year + ' 年 ' + month + ' 月'
        context['title'] = title
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blogs/detail.html'
    context_object_name = 'post'
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.increase_viewers()
        return response

    def get_object(self, queryset=None):
        post = super().get_object(queryset=None)
        post.body = markdown.markdown(post.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        title = self.object.title
        context.update({
            'form': form,
            'comment_list': comment_list,
            'title': title,
        })
        return context

def index(request):
    post_list = Post.objects.all()
    context = {'post_list': post_list,
            'title': 'Black & White',
            }
    return render(request, 'blogs/index.html', context=context)

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_viewers()
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
