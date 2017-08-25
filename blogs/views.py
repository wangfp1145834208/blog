from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {'title': '首页',
            'welcome': '欢迎～'}
    return render(request, 'blogs/index.html', context=context)
