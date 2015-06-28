#coding=UTF-8
__author__ = 'karottc'

import logging
import time
import sys
import urllib2
import json
import MySQLdb
import copy

reload(sys)
sys.setdefaultencoding('utf-8')


user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"

headers = {"User-agent": user_agent}

#db = MySQLdb.connect("localhost","testuser","test123","TESTDB" )
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

def UpdateDatabase(content, type=1):
    try:
        if 1 == type:
            sql = '''replace into t_zhihu_daily_index(fupdatetime,fstoryid,ftitlename,fnum,frecomm,ftitlepic,ftitlebigpic,fdisplaydate) \
                     values(%(updatetime)d, %(storyid)d, '%(titlename)s', %(num)d, '%(recomm)s','%(titlepic)s', '%(titlebigpic)s','%(displaydate)s')''' % content
        else:
            sql = '''replace into t_zhihu_daily_story(fstoryid,ftitle,fnum,fanwser,fviewmore) \
                    values(%(storyid)d, '%(title)s', %(num)d, '%(answer)s', '%(viewmore)s')''' % content
        cursor.execute(sql)
        db.commit()
        logging.info(sql)
    except Exception, e:
        logging.error(e)
        logging.error(sql)
        db.rollback()

# 每天插入之前先查询数据是否存在
def QueryDatabase(id):
    dictRet = {}
    sql = 'select *from t_zhihu_daily_index where fstoryid=%d' % id
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        nRow = len(results)
        dictRet['ret'] = 0
        dictRet['num'] = nRow
    except Exception, e:
        logging.error(e)
        dictRet['ret'] = 1

    return dictRet


def GetStory(id):
    url = "http://news-at.zhihu.com/api/4/story/%s" % id
    result = URLRequest(url)
    if 0 != result['ret']:
        print 'error'
        sys.exit()
    body = result['body'].replace('\r','')
    bodylines = body.split('\n')
    flagAnswer = 0
    listAnswer = []
    dictAnswer = {}
    answer = ""
    nQuestion = 0
    for line in bodylines:
        if line.find('<h2 class="question-title">') != -1:
            title = line.replace('<h2 class="question-title">','')
            title = title.replace('</h2>','')
            #dictAnswer['title'] = title
            continue
        if line.find('<img class="avatar"') != -1:
            avatar = line.replace('<img class="avatar" src="','')
            avatar = avatar.replace('">','')
            dictAnswer['avatar'] = avatar
            continue
        if line.find('<span class="author">') != -1:
            tempList = line.split('span')
            author = tempList[1].replace(' class="author">','')
            # 区分有无个性签名的情况
            if line.find('bio') != -1:
                author = author.replace('，</','')
                bio = tempList[3].replace(' class="bio">','')
                bio = bio.replace('</','')
            else:
                author = author.replace('</','')
                bio = ""
            dictAnswer['author'] = author
            dictAnswer['bio'] = bio
        if line == '<div class="content">':
            flagAnswer = 1
        elif flagAnswer == 1 and line != '</div>':
            #str = "%s\n" % line
            line = line.replace('<p>','')
            line = line.replace('</p>','')
            line = line.replace('&hellip;', '...')
            if line.find('<img class="content-image"') != -1:
                tempList = line.split('"')
                line = '<img src="%s" />' % tempList[3]
            answer += "%s\n" % line
            #print line
        elif flagAnswer == 1 and line == '</div>':
            dictAnswer['answer'] = answer
            listAnswer.append(copy.deepcopy(dictAnswer))
            dictAnswer.clear()
            flagAnswer = 0
            answer = ""
            continue
        if line.find('<div class="view-more">') != -1:
            tempList = line.split('"')
            moreUrl = tempList[3]

            strAnswer = json.dumps(listAnswer, ensure_ascii=False)

            database = {}
            database['storyid'] = id
            database['title'] = title
            database['num'] = len(listAnswer)
            database['answer'] = strAnswer
            database['viewmore'] = moreUrl
            UpdateDatabase(database, 2)
            answer = ""
            del listAnswer[:]
            nQuestion += 1

    dictRet = {}
    strComm = ""
    if result.has_key('recommenders'):
        for val in result["recommenders"]:
            strComm += '%s,' % val["avatar"]
    dictRet['recomm'] = strComm
    strImge = ""
    if result.has_key('image'):
        strImge = result["image"]
    dictRet['bigpic'] = strImge
    dictRet['num'] = nQuestion
    return dictRet


def GetIndex():
    originUrl = "http://news-at.zhihu.com/api/4/section/2"

    result = URLRequest(originUrl)
    if 0 != result['ret']:
        print 'error'
        sys.exit()
    dictContent = result['stories'][0]
    endTime = result['timestamp'] - 30 * 60    # 延迟半小时
    existRet = QueryDatabase(dictContent['id'])
    if 0 != existRet['ret'] or 0 != existRet['num']:
        logging.error("%d is already exist." % dictContent['id'])
        return

    thisTime = endTime + (len(result['stories']) - 1) * 24 * 3600
    strTemp = '%d,date=%s,id=%d, title=%s,image=%s' % (thisTime, dictContent['display_date'],dictContent['id'], dictContent['title'],dictContent['images'][0])
    logging.info(strTemp)
    dictRet = GetStory(dictContent['id'])
    data = {}
    data['updatetime'] = thisTime
    data['storyid'] = dictContent['id']
    data['titlename'] = dictContent['title']
    data['titlepic'] = dictContent['images'][0]
    data['displaydate'] = dictContent['display_date']
    data['num'] = dictRet['num']
    data['recomm'] = dictRet['recomm']
    data['titlebigpic'] = dictRet['bigpic']
    UpdateDatabase(data, 1)


if __name__ == '__main__':
    Init()
    GetIndex()
    #QueryDatabase(375)

endTime = time.time()
seconds = endTime - startTime
mins = seconds / 60
strCost = "time cose=%d s = %d mins" % (seconds, mins)
print strCost
logging.info(strCost)

db.close()