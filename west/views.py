#coding=UTF-8
from django.http import HttpResponse
import json
import simplejson
#from django.utils import simplejson

def first_page(request):
    return HttpResponse("<p>西餐</p>")

def staff(request):
    result = {}
    result['id'] = 1234
    result['title'] = "主题没想好"
    result['content'] = "内容也没有"
    #print request
    try:
        req = request.GET['id']
        if req != "":
            print req
        else:
            print 'no id content'
    except Exception, e:
        print e
    #print request.GET['id']
    #return HttpResponse(json.dumps(result))
    #return HttpResponse(json.dumps(result),content_type="application/json")
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json; charset=utf-8")
    #return HttpResponse(simplejson.dumps(result, ensure_ascii=False))

# Create your views here.
