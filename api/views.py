#coding=UTF-8
__author__ = 'karottc'

from django.http import HttpResponse
import json
import sys
from querydb import *

reload(sys)
sys.setdefaultencoding('utf-8')

def GetHomeList(request):
    qd = QueryDB()
    content = {}

    listStory = qd.QueryIndex()
    content['number'] = len(listStory)
    content['ret'] = 0
    content['err'] = ""
    content['stories'] = listStory
    result = json.dumps(content, ensure_ascii=False)
    logging.info(result)
    return HttpResponse(result, content_type='application/json; charset=utf-8')

def GetNextList(request):
    qd = QueryDB()

    content = {}
    content['ret'] = 0
    content['err'] = ""
    try:
        id = int(request.GET['timestamp'])
        listStory = qd.QueryIndex(id)
        content['number'] = len(listStory)
        content['err'] = ""
        content['ret'] = 0
        content['stories'] = listStory
    except Exception, e:
        content['number'] = 0
        content['err'] = str(e)
        content['ret'] = 1
    result = json.dumps(content, ensure_ascii=False)
    logging.info(result)
    return HttpResponse(result, content_type='application/json; charset=utf-8')

def GetStoryDetail(request):
    qd = QueryDB()

    content = {}

    content['ret'] = 0
    content['err'] = ""
    try:
        id = int(request.GET['id'])
        listStory = qd.QueryStory(id)
        content['question_num'] = len(listStory)
        content['err'] = ""
        content['ret'] = 0
        content['stories'] = listStory
    except Exception, e:
        content['number'] = 0
        content['err'] = str(e)
        content['ret'] = 1
        print e
    result = json.dumps(content, ensure_ascii=False)
    logging.info(result)
    return HttpResponse(result, content_type='application/json; charset=utf-8')