#coding=UTF-8

from django.http import HttpResponse

def first_page(request):
    return HttpResponse("<p>美好的事情总会发生！</p>")
