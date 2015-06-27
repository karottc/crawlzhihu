#coding=UTF-8
from django.http import HttpResponse
import simplejson


def GetHomeList(request):
    content = {}

    content['number'] = 20
    content['ret'] = 0
    content['err'] = ""
    result = simplejson.dumps(content, ensure_ascii=False)
    return HttpResponse(result, content_type='application/json; charset=utf-8')

def GetNextList(request):
    content = {}
    content['number'] = 20
    content['ret'] = 0
    content['err'] = ""
    try:
        id = int(request.GET['timestamp'])
    except Exception, e:
        content['number'] = 0
        content['err'] = str(e)
        content['ret'] = 1
    result = simplejson.dumps(content, ensure_ascii=False)
    return HttpResponse(result, content_type='application/json; charset=utf-8')
