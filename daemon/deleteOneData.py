#coding=UTF-8
__author__ = 'karottc'

import logging
import time
import sys
import urllib2
import MySQLdb
import json


reload(sys)
sys.setdefaultencoding('utf-8')

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"

headers = {"User-agent": user_agent}

db = MySQLdb.connect("localhost","root","","zhihu", use_unicode=True, charset="utf8")

# 使用cursor()方法获取操作游标
cursor = db.cursor()

now = time.time()
year, mon, day, hour, minutes, val, val, val, val = time.localtime(now)

startTime = now

def Init():
    logPath = '/root/testproject/mysite/log/zhihu_%d%02d%02d.log' % (year, mon, day)
    logPath = 'zhihu_%d%02d%02d.log' % (year, mon, day)
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(funcName)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=logPath,
                filemode='a')

def URLRequest(url):
    try:
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        content = json.loads(response.read())
        content['ret'] = 0
        return content
    except Exception, e:
        print e
        logging.error(e)
        return {'ret':1, 'err':'request exception'}

def DeleteDatabase(id):
    try:
        sqlIndex = "delete from t_zhihu_daily_index where fstoryid=%d" % id
        sqlStory = "delete from t_zhihu_daily_story where fstoryid=%d" % id

        cursor.execute(sqlIndex)
        cursor.execute(sqlStory)

        db.commit()
        logging.info(sqlIndex)
        logging.info(sqlStory)
    except Exception, e:
        logging.error(e)
        #logging.error(sql)
        db.rollback()

def GetIndex():
    originUrl = "http://news-at.zhihu.com/api/4/section/2"

    result = URLRequest(originUrl)
    if 0 != result['ret']:
        print 'error'
        sys.exit()
    dictContent = result['stories'][0]
    DeleteDatabase(dictContent['id'])
    logging.info('done.')
    print "done"


if __name__ == '__main__':
    Init()
    GetIndex()

endTime = time.time()
seconds = endTime - startTime
mins = seconds / 60
strCost = "time cose=%d s = %d mins" % (seconds, mins)
print strCost
logging.info(strCost)

db.close()