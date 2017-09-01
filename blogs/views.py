from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils.text import slugify
from django.db.models import Q
import markdown
from markdown.extensions.toc import TocExtension

from comments.forms import CommentForm
from .models import Post, Category, Tag

class IndexView(ListView):
    model = Post
    template_name = 'blogs/index.html'
    context_object_name = 'post_list'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page = context['page_obj']
        is_paginated = context['is_paginated']
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)
        title = 'Black & White'
        context.update({'title': title})
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}
        left_has_more = False
        right_has_more = False
        size = 2
        left = []
        right = []
        page_number = page.number
        total_pages = paginator.num_pages
        if page_number == 1:
            if total_pages - page_number <= size:
                right.extend(range(2, total_pages + 1))
            else:
                right.extend(range(2, 3))
                right_has_more = True
        elif page_number < total_pages:
            if page_number - 1 <= size:
                left.extend(range(1, page_number))
            else:
                left.extend(range(page_number - size + 1, page_number))
                left_has_more = True
            if total_pages - page_number <= size:
                right.extend(range(page_number + 1, total_pages + 1))
            else:
                right.extend(range(page_number + 1, page_number + size))
                right_has_more = True
        else:
            if page_number - 1 <= size:
                left.extend(range(1, page_number))
            else:
                left.extend(range(page_number - size + 1, page_number))
                left_has_more = True
        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
        }
        return data

class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs['pk'])
        return super().get_queryset().filter(category=cate)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        context = super().get_context_data(**kwargs)
        year = self.kwargs['year']
        month = self.kwargs['month']
        title = year + ' 年 ' + month + ' 月'
        context['title'] = title
        return context

class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs['pk'])
        return super().get_queryset().filter(tags=tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = Tag.objects.get(pk=self.kwargs['pk'])
        title = tag.name + '_标签'
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
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        post.toc = md.toc
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

def search(request):
    q = request.GET['q']
    error_msg = ''
    title = '搜索'

    if not q:
        error_msg = "请输入关键词"
        return render(request, 'blogs/index.html', {'error_msg': error_msg,
                                                    'title': title})
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blogs/index.html', {'error_msg': error_msg,
                                                'post_list': post_list,
                                                'title': title})

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
