from django.http import HttpResponse

def first_page(request):
    return HttpResponse('<p>welcome</p>')
